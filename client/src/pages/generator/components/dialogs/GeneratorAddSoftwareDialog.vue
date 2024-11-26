<script setup lang="ts">

import {useDialogPluginComponent, useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, ref, onBeforeMount} from "vue";
import _, {random} from "lodash";
import {api} from "boot/axios";

const generatorViewStore = useGeneratorViewStore();

const {
  disciplineSoftware,
} = storeToRefs(generatorViewStore)

defineEmits([
  ...useDialogPluginComponent.emits
])

const $q = useQuasar()
const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

const correct = computed(() => {
  if (clicense__name.value == '') return true

  return false
})

const clicense__name = ref<string>('')

async function onOKClick() {
  $q.loading.show({message: "Сохранение"})

  disciplineSoftware.value[0]?.value.push({
    id: Math.floor(Math.random() * 100000),
    clicense__name: clicense__name.value,
  })

  $q.loading.hide()
  onDialogOK()
}

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide" persistent>
    <q-card class="q-dialog-plugin" style="width: 700px;">
      <div class="q-ma-md">
        <div class="q-mt-md q-gutter-md">
          <q-input
              label="Наименование ПО"
              v-model="clicense__name"
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
