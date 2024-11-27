<script setup lang="ts">


import {useDialogPluginComponent, useQuasar} from "quasar";
import {api} from "boot/axios";
import {ref} from "vue";

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

const props = defineProps({
  id: {
    required: true,
    type: Number,
  }
})

const comment = ref('')
const oldCommentView = ref(false)
const oldComments = ref([])

const protocolNumber = ref()
const protocolDate = ref()
const acceptRPD = ref(false)
const $q = useQuasar()

async function getRPD() {
  window.location.href = `/api/generator/${props.id}/get-rpd-report/`
}

async function getAnnot() {
  window.location.href = `/api/generator/${props.id}/get-rpd-annotation/`
}

async function onAcceptClick() {
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

</script>

<template>

  <q-dialog ref="dialogRef" @hide="onDialogHide" persistent>
    <q-card class="q-dialog-plugin" style="width: 700px;">
      <q-card-section>
        <div class="text-h6">Просмотр РПД</div>
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

      <q-card-section>
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
        <q-btn flat color="teal" label="Утвердить" @click="acceptRPD = true"/>
        <q-btn flat color="warning" label="Отправить на доработку" @click="onRefileClick"/>
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
      </q-card-section>

      <q-card-actions align="right" class="bg-white text-teal">
        <q-btn flat label="Закрыть" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>

  <q-dialog v-model="acceptRPD">
    <q-card>
      <q-card-section>

      </q-card-section>
      <q-card-actions align="right">
        <q-btn flat color="secondary" label="Утвердить"/>
        <q-btn flat color="negative" label="Отмена" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
