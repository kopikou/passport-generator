<script setup lang="ts">


import {useDialogPluginComponent, useQuasar} from "quasar";
import {api} from "boot/axios";
import {computed, ref, watch} from "vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import EmptyIcon from "components/EmptyIcon.vue";
import NoCommentsIcon from "components/NoCommentsIcon.vue";
import useMainStore from "stores/mainStore";

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

const mainStore = useMainStore();

const {FORCE_SCRIPT_NAME} = storeToRefs(mainStore);

const generatorViewStore = useGeneratorViewStore();

const props = defineProps({
  id: {
    required: true,
    type: Number,
  },
  data: {
    required: true,
  }
})

const $q = useQuasar()

const comment = ref('')
const oldCommentView = ref(false)
const oldComments = ref([])

const disabled = computed(() => {
  if (!protocolNumber.value) return true
  if (!protocolDate.value) return true
  if (!meeting.value) return true

  return false
})
const protocolNumber = ref($q.localStorage.getItem('rpd_protocolNumber'))
const protocolDate = ref($q.localStorage.getItem('rpd_protocolDate'))
const acceptRPD = ref(false)
const userType = ref(0)

const bothAcceptAndConfirm = ref(false);
const meeting = ref($q.localStorage.getItem('rpd_meeting') || "заседании кафедры")
const userTypeOptions = [
  {value: 0, label: 'Руководитель программы'},
  {value: 1, label: 'Заведующий кафедрой'},
  // {value: 2, label: 'Директор института'},
]


watch([meeting, protocolNumber, protocolDate], () => {
  $q.localStorage.set('rpd_meeting', meeting.value);
  $q.localStorage.set('rpd_protocolNumber', protocolNumber.value);
  $q.localStorage.set('rpd_protocolDate', protocolDate.value);
})

const canSendToRefill = computed(() => {
    return props.data.status == 2 &&
      (
        (props.data.type.includes('rop') && !props.data.user_confirmed)
        || (props.data.type.includes('zav') && !props.data.user_accepted)
      )
})

async function getRPD() {
  window.location.href = `${FORCE_SCRIPT_NAME.value}/api/generator/${props.id}/get-rpd-report/`
}

async function getAnnot() {
  window.location.href = `${FORCE_SCRIPT_NAME.value}/api/generator/${props.id}/get-rpd-annotation/`
}

async function onAcceptClick() {
  if (bothAcceptAndConfirm.value) {
    await api.post(`/api/generator/${props.id}/confirm-rpd/`)
  }

  await api.post(`/api/generator/${props.id}/accept-rpd/`, {
    date: protocolDate.value,
    number: protocolNumber.value,
    userType: userType.value,
    meeting: meeting.value,
  })
  onDialogOK()
}

async function onAcceptButtonClick() {
  bothAcceptAndConfirm.value = false;
  acceptRPD.value = true;
}

async function onAcceptConfirmButtonClick() {
  bothAcceptAndConfirm.value = true;
  acceptRPD.value = true;
}

async function onConfirmButtonClick() {
  bothAcceptAndConfirm.value = false;
  let r = await api.post(`/api/generator/${props.id}/confirm-rpd/`)
  onDialogOK()
}

async function onRefileClick() {
  bothAcceptAndConfirm.value = false;
  let r = await api.post(`/api/generator/${props.id}/send-rpd-on-refile/`, {comment: comment.value})
  onDialogOK()
}

async function getOldComment() {
  $q.loading.show({message: "Загрузка прошлых комментариев"})
  let r = await api.get(`/api/generator/${props.id}/get-old-comments/`)
  oldComments.value = r.data
  $q.loading.hide()
  oldCommentView.value = true
}

function translateDate(date) {
  let result = new Date(date).toLocaleString('ru')
  return result
}

function getStatusColor(status) {
  switch (status) {
    case 0:
      return ''
    case 1:
      return 'bg-accent text-white'
    case 2:
      return 'bg-secondary text-white'
    case 3:
      return 'bg-positive text-white'
    case 4:
      return 'bg-warning text-white'
  }
}

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide" persistent>
    <q-card class="q-dialog-plugin" style="width: 700px; max-width: 80vw;">
      <q-card-section>
        <div class="text-h6">
          {{ data.abbr }}-{{ data.yr }} - {{ data.discpl }}
        </div>
        <div class="text-subtitle2">Составитель:
          <q-chip style="max-width: 500px" square :label="props.data.person">
            <q-tooltip>
              {{ props.data.person }}
            </q-tooltip>
          </q-chip>
        </div>
        <div class="text-subtitle2">Текущий статус:
          <q-chip style="max-width: 500px" :class="getStatusColor(props.data.status)" square
                  :label="props.data.status_verbose">
            <q-tooltip>
              {{ props.data.status_verbose }}
            </q-tooltip>
          </q-chip>
        </div>
      </q-card-section>

      <q-card-section>

        <div class="row">
          <q-btn
            class="col"
            label="Открыть файл РПД"
            :href="`${FORCE_SCRIPT_NAME}/api/generator/${props.id}/get-rpd-report/`"
            target="_blank"
          />
          <!--          <q-btn-->
          <!--            class="col"-->
          <!--            label="Аннотация"-->
          <!--            :href="`${FORCE_SCRIPT_NAME}/api/generator/${props.id}/get-rpd-annotation/`"-->
          <!--            target="_blank"-->
          <!--          />-->
        </div>
      </q-card-section>
      <q-card-section v-if="props.data.status != 3">
        <q-input
          label="Комментарий"
          v-model="comment"
          stack-label
          filled
          type="textarea"
        />
      </q-card-section>
      <q-card-section>
        <q-btn
          label="Прошлые комментарии"
          style="width: 100%"
          color="primary"
          @click="getOldComment"
        />
      </q-card-section>

      <q-card-section style="display: flex; gap: 8px; justify-content: space-between">
        <template v-if="data.status == 2 || data.status == 3">
          <q-btn v-if="data.type.includes('rop') && data.type.includes('zav')" flat class="bg-light-green-1"
                 color="light-green-8"
                 @click="onAcceptConfirmButtonClick" :disable="!!data.user_accepted">
            <div v-if="data.user_accepted">
              Согласован и утвержден <br>{{ data.user_accepted_name }}
            </div>
            <div v-else>
              Согласовать и утвердить
            </div>
          </q-btn>

          <template v-else>
            <q-btn flat class="bg-light-green-1" color="light-green-8"
                   @click="onAcceptButtonClick" :disable="!data.type.includes('zav') || !!data.user_accepted">
              <div v-if="data.user_accepted">
                Утвержден <br>{{ data.user_accepted_name }}
              </div>
              <div v-else>
                <template v-if="data.type.includes('zav')">Утвердить</template>
                <template v-else>Не утвержден</template>
              </div>
            </q-btn>
            <q-btn  flat class="bg-light-green-1" color="light-green-8"
                   @click="onConfirmButtonClick" :disable="!data.type.includes('rop') ||!!data.user_confirmed">
              <div v-if="data.user_confirmed">
                Согласован <br>{{ data.user_confirmed_name }}
              </div>
              <div v-else>
                <template v-if="data.type.includes('rop')">Согласовать</template>
                <template v-else>Не согласован</template>
              </div>
            </q-btn>
          </template>
        </template>
          <q-btn  v-if="canSendToRefill" flat class="bg-amber-1 " color="amber-8" label="Отправить на доработку"
                 @click="onRefileClick"/>
          <q-btn  flat class="bg-grey-3" color="silver" label="Отмена" @click="onDialogCancel"/>
      </q-card-section>
    </q-card>
  </q-dialog>

  <q-dialog v-model="oldCommentView">
    <q-card>
      <q-card-section>
        <div class="text-h6">Прошлые комментарии</div>
      </q-card-section>

      <q-card-section class="bg-grey-2" v-for="item in oldComments" v-if="oldComments.length != 0">
        <div class="text-subtitle1">{{ translateDate(item.created_at) }}</div>
        <div>
          {{ item.comment }}
        </div>
      </q-card-section>
      <q-card-section v-else>
        <div class="text-subtitle1">
          Комментариев нет
        </div>
        <no-comments-icon/>
      </q-card-section>

      <q-card-actions align="right" class="bg-white text-teal">
        <q-btn flat label="Закрыть" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="acceptRPD">
    <q-card style="width: 500px">
      <q-card-section>
        <div class="text-h6">
          Утверждение РПД
        </div>
      </q-card-section>
      <q-card-section>
        <div class="q-gutter-md">
          <q-select
            v-model="userType"
            label="Кто утвердил"
            :options="userTypeOptions"
            stack-label
            map-options
            emit-value
            filled
          />
          <q-input
            v-model="meeting"
            type="text"
            stack-label
            label="Утвердили на"
            filled
          />
          <q-input
            v-model="protocolNumber"
            type="text"
            stack-label
            label="Номер протокола"
            filled
          />
          <q-input
            v-model="protocolDate"
            type="date"
            stack-label
            label="Дата протокола"
            filled
          />
        </div>
      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat color="secondary" label="Утвердить" :disable="disabled" @click="onAcceptClick" v-close-popup/>
        <q-btn flat color="negative" label="Отмена" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
