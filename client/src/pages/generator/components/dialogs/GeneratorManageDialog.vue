<script setup lang="ts">


import {useDialogPluginComponent, useQuasar} from "quasar";
import {api} from "boot/axios";
import {computed, ref} from "vue";
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

const comment = ref('')
const oldCommentView = ref(false)
const oldComments = ref([])

const disabled = computed(() => {
  if (!protocolNumber.value) return true
  if (!protocolDate.value) return true
  if (!meeting.value) return true
  if (!userType.value) return true

  return false
})
const protocolNumber = ref()
const protocolDate = ref()
const acceptRPD = ref(false)
const userType = ref(0)
const meeting = ref()
const userTypeOptions = [
  {value: 0, label: 'Руководитель программы'},
  {value: 1, label: 'Заведующий кафедрой'},
  {value: 2, label: 'Директор института'},
]

const $q = useQuasar()

async function getRPD() {
  window.location.href = `${FORCE_SCRIPT_NAME.value}/api/generator/${props.id}/get-rpd-report/`
}

async function getAnnot() {
  window.location.href = `${FORCE_SCRIPT_NAME.value}/api/generator/${props.id}/get-rpd-annotation/`
}

async function onAcceptClick() {
  let r = await api.post(`/api/generator/${props.id}/accept-rpd/`, {
    date: protocolDate.value,
    number: protocolNumber.value,
    userType: userType.value,
    meeting: meeting.value,
  })
  onDialogOK()
}

async function onRefileClick() {
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
    <q-card class="q-dialog-plugin" style="width: 700px;">
      <q-card-section>
        <div class="text-h6">Просмотр РПД
          <q-chip style="max-width: 500px" :label="`${props.data.abbr}-${props.data.yr} ${props.data.discpl}`" square>
            <q-tooltip>
              {{ props.data.abbr }}-{{ props.data.yr }} {{ props.data.discpl }}
            </q-tooltip>
          </q-chip>
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

        <div class="row q-gutter-x-md">
          <q-btn
            class="col"
            label="РПД"
            @click="getRPD"
          />
          <q-btn
            class="col"
            label="Аннотация"
            @click="getAnnot"
          />
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

      <q-card-actions align="right">
        <q-btn flat color="teal" label="Утвердить" @click="acceptRPD = true" :disable="props.data.status == 3"/>
        <q-btn flat color="warning" label="Отправить на доработку" @click="onRefileClick"
               :disable="props.data.status == 3"/>
        <q-btn flat color="red" label="Отмена" @click="onDialogCancel"/>
      </q-card-actions>
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
            label="Заседание"
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
