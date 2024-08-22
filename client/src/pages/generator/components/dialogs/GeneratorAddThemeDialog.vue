<script setup lang="ts">

import {useDialogPluginComponent} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, ref} from "vue";

const generatorViewStore = useGeneratorViewStore();
const {
  formControl,
} = storeToRefs(generatorViewStore)

defineEmits([
  ...useDialogPluginComponent.emits
])

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

const props = defineProps({
  id: {
    required: true,
  }
})

const themeName = ref('')
const hourCount = ref(0)
const control = ref()

const correct = computed(() => {
  if (hourCount.value <= 0) return true
  if (themeName.value.length < 3) return true
  if (control.value == null) return true

  return false
})

async function onOKClick() {

  onDialogOK()
}

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <div class="q-pa-md q-gutter-md">
        <q-chip color="teal" class="text-subtitle1">Семестр {{ id }}</q-chip>
        <q-input
            stack-label
            label="Название темы"
            v-model="themeName"
            filled
            :rules="[ val => val.length >= 4 || 'Введите больше 3-ех символов']"
            type="textarea"
        />
        <q-input
            stack-label
            label="Количество часов"
            v-model="hourCount"
            filled
            type="number"
            :rules="[ val => val > 0 || 'Введите значение больше 0']"
        />
        <q-select
            stack-label
            label="Форма контроля"
            filled
            :options="formControl"
            v-model="control"
            option-label="name"
            option-value="id"
            map-options
            emit-value
        />
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
