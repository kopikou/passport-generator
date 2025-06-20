<script setup lang="ts">

import {useQuasar} from "quasar";
import {api} from "boot/axios";
import {onBeforeMount, ref, watch, watchEffect} from "vue";
import {GeneratorSoftwareData} from "src/types";
import _ from "lodash";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import GeneratorAddSoftwareDialog from "pages/generator/components/dialogs/GeneratorAddSoftwareDialog.vue";

const $q = useQuasar()
const generatorViewStore = useGeneratorViewStore()

const {
  activeRpdId,
  disciplineSoftware,
  rpdData,
  disabled,
  abortGetDataController,
} = storeToRefs(generatorViewStore)

const searchVal = ref('')
const searchResult = ref<GeneratorSoftwareData[]>([])
const softwareData = ref<GeneratorSoftwareData[]>([])

function checkTaken(id) {
  return _.map(softwareData.value, (x) => x.id).includes(id);
}

function addSoftware(data) {
  softwareData.value.push(data)
  saveSoftware()
}

function deleteSoftware(item) {
  $q.dialog({
    title: 'Подтвердите',
    message: `Вы точно хотите удалить "${item.clicense__name}"?`,
    cancel: "Отмена",
    ok: "Удалить"
  }).onOk(() => {
    softwareData.value = softwareData.value.filter(x => x != item)
    saveSoftware()
  })
}

async function saveSoftware() {
  // $q.loading.show()
  if (generatorViewStore.abortGetDataController)
    generatorViewStore.abortGetDataController.abort()

  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: "software",
    value: softwareData.value,
  })
  // _.set(disciplineSoftware.value, "[0].value", softwareData.value)
  await generatorViewStore.getData()
  generatorViewStore.checkErrors()
  // $q.loading.hide()
}


async function searchSoft() {
  if (searchVal.value.length <= 3) {
    $q.notify({
      message: "Введите больше 3-ех символов",
      color: "negative",
    })
  } else {
    $q.loading.show({message: "Поиск программного обеспечения"})
    let r = await api.get('/api/generator/search-software/', {params: {val: searchVal.value}})
    searchResult.value = r.data
    $q.loading.hide()
  }
}

function addPO() {
  // if (!disciplineSoftware.value[0]) {
  //   _.set(disciplineSoftware.value, "[0].value", [])
  //   saveSoftware()
  // }
  $q.notify({
    message: "Убедитесь, что выбранный источник доступен всем студентам и в достаточном количестве.",
    color: "secondary",
    type: "info",
    position: "top",
    progress: true,
    timeout: 3500,
  })

  $q.dialog({
    component: GeneratorAddSoftwareDialog,
  }).onOk((data) => {
    addSoftware(data);
  })
}

function addDefaultPO() {
  softwareData.value.push({clicense__name: `Системное программное обеспечение`, clicense__type: 'Лицензионное'})
  softwareData.value.push({clicense__name: `Пакет прикладных офисных программ`, clicense__type: 'Лицензионное'})
  softwareData.value.push({clicense__name: `Интернет-браузер`, clicense__type: 'Лицензионное'})
  // oborudData.value.push({name: `Учебная аудитория для проведения лабораторных/практических (семинарских) занятий, групповых и индивидуальных консультаций, текущего контроля и промежуточной аттестации. Оснащение: комплект учебной мебели, рабочее место преподавателя, доска. Мультимедийное оборудование (в том числе переносное): мультимедийный проектор, экран, акустическая система, компьютер с выходом в интернет. Рабочие места обучающихся, оснащенные компьютерами с выходом в интернет.`})
  saveSoftware()
}

watch(disciplineSoftware, () => {
  softwareData.value = disciplineSoftware.value[0]?.value || []
}, {
  immediate: true
})

</script>

<template>
  <div class="q-px-md">
    <span class="text-h6">Перечень лицензионного программного обеспечения для дисциплины</span>
    <p></p>
    <q-separator class="q-mt-md q-mb-md"/>
    <q-btn
      class="q-mb-md"
      label="Добавить ПО"
      color="secondary"
      @click="addPO"
      v-show="!disabled"
    />
    <q-btn
      class="q-mb-md q-ml-sm"
      label="Добавить ПО по-умолчанию"
      color="purple-2"
      text-color="black"
      no-caps
      @click="addDefaultPO"
      v-show="!disabled"
    />
    <div class="row q-gutter-x-md q-mb-md" v-show="!disabled">
      <q-input
        label="Введите текст для поиска"
        stack-label
        v-model="searchVal"
        filled
        class="col"
        :rules="[ val => val.length >= 4 || 'Введите больше 3-ех символов']"
      />
      <q-btn color="secondary" @click="searchSoft" label="Поиск"/>
    </div>
    <div class="row">
      <div class="col-6">
        <div class="text-h6">Выбранный софт</div>
        <div v-for="item in softwareData" style="width: 95%">
          <q-field label="Название" stack-label filled class="q-mb-md">
            <template #control>
              <div class="text-subtitle1 self-center full-width no-outline">
                <span>{{ item.clicense__name }}</span>
                <q-chip v-if="item.clicense__type">{{ item.clicense__type }}</q-chip>
              </div>
            </template>
            <template v-slot:append>
              <q-btn color="red-7" flat round densed icon="mdi-close" @click="deleteSoftware(item)" v-show="!disabled">
              </q-btn>
            </template>
          </q-field>
        </div>
      </div>
      <div class="col-6">
        <div v-for="item in searchResult">
          <q-field label="Название" stack-label filled class="q-mb-md">
            <template #control>
              <div class="text-subtitle1 self-center full-width no-outline">
                <span>{{ item.clicense__name }}</span>
              </div>
              <div class="q-gutter-x-md q-mt-md">
                <q-btn :disable="checkTaken(item.id)" color="primary" label="Добавить" @click="addSoftware(item)"/>
              </div>
            </template>
          </q-field>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
