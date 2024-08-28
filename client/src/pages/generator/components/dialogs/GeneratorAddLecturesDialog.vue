<script setup lang="ts">

import {useDialogPluginComponent, useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, ref} from "vue";
import {api} from "boot/axios";
import _ from "lodash";

defineEmits([
  ...useDialogPluginComponent.emits
])

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()
const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore();

const {
  rpdData,
  disciplineThemes,
} = storeToRefs(generatorViewStore)

const props = defineProps({
  id: {
    required: true,
  },
  sem: {
    require: true
  }
})

const name = ref('')
const hourCount = ref(0)
const theme = ref()

const correct = computed(() => {

  if (!name.value || name.value.length < 3) return true
  else if (!hourCount.value || hourCount.value <= 0) return true
  else if (!theme.value) return true

  return false
})

async function onOKClick() {
  $q.loading.show({message: "Сохранение"})
  let r = await api.post('/api/generator/save-discipline-work-hour/', {
    planlineslink_id: rpdData.value.id,
    theme_id: theme.value,
    type: 0,  // Лекции
    name: name.value,
    hours: hourCount.value,
    semester: props.sem,
    id: props.id,
  })

  // if (!props.id) {
  //   rpdData.value.discipline_themes.push(r.data)
  // } else {
  //   rpdData.value.discipline_themes[_.findKey(disciplineThemes.value, (x) => x.id == props.id)] = r.data
  // }

  $q.loading.hide()
  onDialogOK()
}

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin" style="width: 700px;">
      <div class="q-pa-md q-gutter-md">
        <q-chip color="teal" class="text-subtitle1">Семестр {{ sem }}</q-chip>
        <q-input
          v-model="name"
          stack-label
          label="Наименование лекционной работы"
          filled
          :rules="[ val => val.length >= 4 || 'Введите больше 3-ех символов']"
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
          :options="disciplineThemes"
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
