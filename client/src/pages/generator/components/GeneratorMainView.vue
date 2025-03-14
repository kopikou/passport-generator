<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, onBeforeMount, ref, watch, watchEffect} from "vue";
import _ from "lodash";
import {api} from "boot/axios";
import {useQuasar} from "quasar";

const generatorViewStore = useGeneratorViewStore()
const $q = useQuasar()
const {
  cafData,
  rpdData,
  semestersData,
  activeRpdId,
  additionalInfo,
  disciplineGoal,
  disabled,
} = storeToRefs(generatorViewStore)

const displGoal = ref()
const saveData = _.debounce(async () => {
  console.log(displGoal)
  saveDiscplineGoal()
}, 1000)

const toolbar = ref([
  ['bold', 'italic', 'strike', 'underline', 'subscript', 'superscript'],
  [
    {
      label: 'Стиль текста',
      icon: 'mdi-format-color-text',
      fixedLabel: true,
      options: ['h4', 'h5', 'h6', 'p', 'code'],
    },
  ],
  [
    {
      label: 'Размер текста',
      icon: 'mdi-format-size',
      fixedLabel: true,
      list: 'no-icons',
      options: ['size-1', 'size-2', 'size-3', 'size-4', 'size-5'],
    },
    'removeFormat'
  ],
  ['quote', 'unordered', 'ordered', 'outdent', 'indent'],
  ['undo', 'redo'],
  ['fullscreen'],
])

async function saveDiscplineGoal() {
  $q.loading.show()
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: "disciplineGoal",
    value: displGoal.value,
  }).then((v) => {
    $q.notify({
      message: "Данные <span class='text-bold'>о цели освоения дисциплины</span> сохранены!",
      color: "secondary",
      position: "bottom",
      html: true,
    })
    let key = _.findKey(additionalInfo.value, (x) => x.id == v.data.id)
    _.set(additionalInfo.value, `[${key}].value`, displGoal.value)
  }, (rej) => {
    $q.notify({
      message: "Данные <span class='text-bold'>о цели освоения дисциплины</span> не сохранены!",
      color: "negative",
      position: "bottom",
      html: true,
    })
  })
  $q.loading.hide()
}

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

watch(additionalInfo, () => {
  displGoal.value = disciplineGoal.value
}, {immediate: true})

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Данные по дисциплине</span>
      <p>Данные для рабочей программы по дисциплине "Базы данных" получены автоматически из учебного плана</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <div class="q-pb-md">
        <span class="text-subtitle1">Наименование дисциплины</span>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">{{ rpdData.planlines?.dis }}</div>
          </template>
        </q-field>
        <span class="text-subtitle1">Профиль/Специальность</span>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">{{ rpdData.admission?.spec_name }}</div>
          </template>
        </q-field>
        <span class="text-subtitle1">Наименование направления</span>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">{{ rpdData.admission?.direct_name }}</div>
          </template>
        </q-field>
        <span class="text-subtitle1">Кафедра</span>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">{{ cafDataById[rpdData.planlines?.caf]?.label }}</div>
          </template>
        </q-field>
      </div>
      <div class="flex justify-center items-center">
        <span class="text-subtitle1">Количество семестров</span>
        <q-field filled dense style="width: 5%" class="q-ml-md q-mr-md">
          <template v-slot:control>
            <div class="self-center full-width no-outline text-center">{{ semestersData.length }}</div>
          </template>
        </q-field>
        <span class="text-subtitle1">Начальный семестр</span>
        <q-field filled dense style="width: 5%" class="q-ml-md">
          <template v-slot:control>
            <div class="self-center full-width no-outline text-center">{{ semestersData[0]?.num }}</div>
          </template>
        </q-field>
      </div>
      <q-separator class="q-mt-md q-mb-md"/>
      <div>
        <q-input
          label="Цель освоения дисциплины"
          type="textarea"
          filled
          stack-label
          v-model="displGoal"
          class="q-mb-md"
          :readonly="disabled"
          hint="Для аннотации"
          debounce="1000"
          @update:modelValue="saveDiscplineGoal"
        />
        <!--        <q-editor-->
        <!--          v-model="displGoal"-->
        <!--          :toolbar="toolbar"-->
        <!--          @update:modelValue="saveData"-->
        <!--        />-->

      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">

</style>
