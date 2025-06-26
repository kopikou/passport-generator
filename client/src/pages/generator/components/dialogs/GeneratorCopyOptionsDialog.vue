<script setup lang="ts">
import {ref, watch} from "vue";
import {CopyOptions} from "src/types";
import _ from "lodash";
import {useDialogPluginComponent} from "quasar";

const {dialogRef, onDialogHide, onDialogOK, onDialogCancel} = useDialogPluginComponent()

const props = defineProps({
  initData: {
    required: true,
    type: Object as () => CopyOptions
  }
})

const data = ref({
  replace: true,
  indicators: true,
  themes: true,
  lections: true,
  labs: true,
  practices: true,
  srs: true,
  additional_info_resources: true,
  additional_info_interactiveMethods: true,
  additional_info_disciplinePlace: true,
  additional_info_software: true,
  additional_info_logistics: true,
  additional_info_guidelines: true,
  additional_info_library: true,
  additional_info_tat: true,
  additional_info_fos: true,
})

const fields = [
  {key: "indicators", title: "Индикаторы"},
  {key: "themes", title: "Темы"},
  {key: "lections", title: "Лекции"},
  {key: "labs", title: "Лабы"},
  {key: "practices", title: "Практики"},
  {key: "srs", title: "СРС"},
  {key: "additional_info_resources", title: "Другие ресурсы используемые по дисциплине"},
  {key: "additional_info_interactiveMethods", title: "Интерактивные методы"},
  {key: "additional_info_disciplinePlace", title: "Место дисциплины в структуре ООП"},
  {key: "additional_info_software", title: "Программное обеспечение"},
  {key: "additional_info_logistics", title: "МТО"},
  {key: "additional_info_guidelines", title: "Методические указания по дисциплине"},
  {key: "additional_info_library", title: "Литература"},
  {key: "additional_info_tat", title: "Типовые оценочные средства по дисциплине"},
  {key: "additional_info_fos", title: "Оценочные материалы по дисциплине"},
]

function setAll(value: Boolean) {
  fields.forEach(f => {
    data.value[f.key] = value;
  })
}

watch(() => props.initData, () => {
  data.value = {...data.value, ..._.cloneDeep(props.initData)};
}, {
  immediate: true
})

defineEmits([
  // REQUIRED; need to specify some events that your
  // component will emit through useDialogPluginComponent()
  ...useDialogPluginComponent.emits
])

</script>

<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin" style="width: 700px">
      <q-card-section>
        <div class="text-h6">
          Настройки копирования
        </div>
      </q-card-section>
      <q-separator/>
      <q-card-section>
        <q-btn @click="setAll(false)">Снять все</q-btn>
        <q-btn @click="setAll(true)" class="q-ml-sm">Поставить все</q-btn>
      </q-card-section>
      <q-separator/>
      <q-card-section>
        <div style="display: grid; grid-template-columns: 1fr 1fr">
          <div v-for="f in fields">
            <q-toggle v-model="data[f.key]" :label="f.title"/>
          </div>
        </div>
      </q-card-section>
      <q-separator/>
      <q-card-section>
        <q-toggle v-model="data['replace']" >Заменить (если активно, то перезапишет все данные, иначе добавит)</q-toggle>
      </q-card-section>
      <q-separator/>
      <q-card-section style="display: flex; justify-content: space-between">
        <q-btn flat color="primary" @click="onDialogOK(data)">Скопировать</q-btn>
        <q-btn flat color="red" @click="onDialogCancel">Отмена</q-btn>
      </q-card-section>
    </q-card>
  </q-dialog>
</template>

<style scoped>

</style>
