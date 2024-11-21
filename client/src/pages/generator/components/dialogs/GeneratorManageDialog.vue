<script setup lang="ts">


import {useDialogPluginComponent} from "quasar";

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

const props = defineProps({
  id: {
    required: true,
    type: Number,
  }
})

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
        />
        <q-btn
          class="col"
          label="Аннотация"
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
