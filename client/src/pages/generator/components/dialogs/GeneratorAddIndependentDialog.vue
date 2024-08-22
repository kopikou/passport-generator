<script setup lang="ts">

import {useDialogPluginComponent} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, ref} from "vue";

const generatorViewStore = useGeneratorViewStore();

const{
  independentTypes,
}=storeToRefs(generatorViewStore)

defineEmits([
  ...useDialogPluginComponent.emits
])

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

const props = defineProps({
  id: {
    required: true,
  }
})

const independent = ref()
const hourCount = ref(0)
const theme = ref()

const correct = computed(() => {

  return false
})

async function onOKClick() {

  onDialogOK()
}

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin" style="width: 700px;">
      <div class="q-pa-md q-gutter-md">
        <q-chip color="teal" class="text-subtitle1">Семестр {{ id }}</q-chip>
        <q-select
          stack-label
          label="Вид самостоятельной работы"
          filled
          :options="independentTypes"
          v-model="independent"
          option-label="name"
          option-value="id"
          map-options
          emit-value
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
          label="Тема дисциплины"
          filled
          :options="[]"
          v-model="theme"
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
