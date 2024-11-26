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

</script>

<template>

  <q-dialog ref="dialogRef" @hide="onDialogHide" persistent>
    <q-card class="q-dialog-plugin q-pt-md q-pl-md q-pr-md" style="width: 700px;">
      <div class="row q-gutter-x-md q-pb-md">
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

      <q-input
        label="Комментарий"
        v-model="comment"
        stack-label
        filled
        type="textarea"
      />
      <q-btn
        label="Прошлые комментарии"
        style="width: 100%"
        color="primary"
        class="q-mt-md"
        @click="oldCommentView = true"
      />

      <q-card-actions align="right">
        <q-btn flat color="teal" label="Утвердить" @click="onAcceptClick"/>
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

      <q-card-section class="q-pt-none">
        Click/Tap on the backdrop.
      </q-card-section>

      <q-card-actions align="right" class="bg-white text-teal">
        <q-btn flat label="Закрыть" v-close-popup/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
