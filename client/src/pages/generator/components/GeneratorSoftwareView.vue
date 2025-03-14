<script setup lang="ts">

import {useQuasar} from "quasar";
import {api} from "boot/axios";
import {onBeforeMount, ref, watch} from "vue";
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

function deleteSoftware(id) {
  let key = _.findKey(softwareData.value, (x) => x.id == id)
  softwareData.value.splice(key, 1)
  saveSoftware()
}

async function saveSoftware() {
  $q.loading.show()
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: "software",
    value: softwareData.value,
  })
  $q.loading.hide()
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
  if (!disciplineSoftware.value[0]) {
    _.set(disciplineSoftware.value, "[0].value", [])
    saveSoftware()
  }
  $q.notify({
    message: "Убедитесь, что выбранный источник доступен всем студентам и в достаточном количестве.",
    color: "secondary",
    type: "info",
    position: "center",
    progress: true,
    timeout: 3500,
  })

    $q.dialog({
    component: GeneratorAddSoftwareDialog,
  }).onOk(() => {
    softwareData.value = disciplineSoftware.value[0]?.value || []
    saveSoftware()
  })
}

onBeforeMount(() => {
  softwareData.value = disciplineSoftware.value[0]?.value || []
})

watch(disciplineSoftware, () => {
  softwareData.value = disciplineSoftware.value[0]?.value || []
})

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Перечень лицензионного программного обеспечения для дисциплины</span>
      <p></p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-btn
          class="q-mb-md"
          label="Добавить ПО"
          color="secondary"
          @click="addPO"
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
        <div class="col-5">
          <div class="text-h6">Выбраный софт</div>
          <div v-for="item in softwareData" style="width: 95%">
            <q-field label="Название" stack-label filled class="q-mb-md">
              <template #control>
                <div class="text-subtitle1 self-center full-width no-outline">
                  <span>{{ item.clicense__name }}</span>
                  <q-chip v-if="item.clicense__type">{{ item.clicense__type }}</q-chip>
                  <div class="q-gutter-x-md q-mt-md" v-show="!disabled">
                    <q-btn color="red" label="Убрать"
                           @click="deleteSoftware(item.id)"/>
                  </div>
                </div>
              </template>
            </q-field>
          </div>
        </div>
        <div class="col-7">
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
  </div>
</template>

<style scoped>

</style>
