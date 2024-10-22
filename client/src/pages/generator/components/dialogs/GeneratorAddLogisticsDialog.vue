<script setup lang="ts">

import {useDialogPluginComponent, useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, ref, onBeforeMount} from "vue";
import _, {random} from "lodash";
import {api} from "boot/axios";

const generatorViewStore = useGeneratorViewStore();

const {

} = storeToRefs(generatorViewStore)

defineEmits([
  ...useDialogPluginComponent.emits
])

const $q = useQuasar()
const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

const correct = computed(() => {
  if (name.value == '') return true

  return false
})

const name = ref<string>('')

async function onOKClick() {
  $q.loading.show({message: "Сохранение"})

  $q.loading.hide()
  onDialogOK()
}

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin" style="width: 700px;">
      <div class="q-ma-md">
        <div class="q-mt-md q-gutter-md">
          <q-input
              label="Наименование материально-технического обеспечения"
              v-model="name"
              stack-label
              filled
              type="text"
          />
        </div>
      </div>
      <q-card-actions align="right">
        <q-btn flat color="teal" label="Сохранить" @click="onOKClick" :disabled="correct"/>
        <q-btn flat color="red" label="Отмена" @click="onDialogCancel"/>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
