<script setup lang="ts">


import {useDialogPluginComponent} from "quasar";
import {api} from "boot/axios";

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

const props = defineProps({
  id: {
    required: true,
    type: Number,
  }
})

async function getRPD() {
  window.location.href = `/api/generator/${props.id}/get-rpd-report/`
}

async function getAnnot() {
  window.location.href = `/api/generator/${props.id}/get-rpd-annotation/`
}

async function onOKClick() {
  onDialogOK()
}

</script>

<template>

  <q-dialog ref="dialogRef" @hide="onDialogHide">
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
        stack-label
        filled
        type="textarea"
      />
      <q-card-actions align="right">
        <q-btn flat color="teal" label="Утвердить" @click="onOKClick"/>
        <q-btn flat color="warning" label="Отправить на доработку" @click="onOKClick"/>
        <q-btn flat color="red" label="Отмена" @click="onDialogCancel"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
