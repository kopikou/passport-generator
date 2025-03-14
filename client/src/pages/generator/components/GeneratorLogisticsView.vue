<script setup lang="ts">

import {useQuasar} from "quasar";
import {onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import {storeToRefs} from "pinia";
import useGeneratorViewStore from "stores/generatorViewStore";
import {GeneratorOborudData} from "src/types";
import _ from "lodash";
import GeneratorAddLogisticsDialog from "pages/generator/components/dialogs/GeneratorAddLogisticsDialog.vue";

const $q = useQuasar()

const searchVal = ref('')
const searchData = ref<GeneratorOborudData[]>([])
const oborudData = ref<GeneratorOborudData[]>([])

const searchType = ref(1)
const typeOptions = [
  {label: 'По кафедре с ограничениям', value: 1, color: 'green'},
  {label: 'По кафедре', value: 2, color: 'blue'},
  {label: 'По университету', value: 3, color: 'red'},
]

const generatorViewStore = useGeneratorViewStore();

const {
  planlinesData,
  disciplineLogistics,
  activeRpdId,
  disabled,
} = storeToRefs(generatorViewStore)

function addOborud(data) {
  oborudData.value.push(data)
  saveOborud()
}

function deleteOborud(id) {
  let key = _.findKey(oborudData.value, (x) => x.id == id)
  oborudData.value.splice(key, 1)
  saveOborud()
}

async function saveOborud() {
  $q.loading.show()
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: "logistics",
    value: oborudData.value,
  })
  $q.loading.hide()
}


async function searchOborud() {
  if (searchVal.value.length <= 3) {
    $q.notify({
      message: "Введите больше 3-ех символов",
      color: "negative",
    })
  } else {
    $q.loading.show({message: "Поиск оборудования"})
    let r = await api.get('/api/generator/search-oborud/', {
      params: {
        val: searchVal.value,
        caf: planlinesData.value.caf,
        type: searchType.value
      }
    })
    searchData.value = r.data
    $q.loading.hide()
  }
}

function checkTaken(id) {
  return _.map(oborudData.value, (x) => x.id).includes(id);
}

function addMTO() {
  if (!disciplineLogistics.value[0]) {
    _.set(disciplineLogistics.value, "[0].value", [])
    saveOborud()
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
    component: GeneratorAddLogisticsDialog,
  }).onOk(() => {
    oborudData.value = disciplineLogistics.value[0]?.value || []
    saveOborud()
  })
}

onBeforeMount(() => {
  oborudData.value = disciplineLogistics.value[0]?.value || []
})

watch(disciplineLogistics, () => {
  oborudData.value = disciplineLogistics.value[0]?.value || []
})

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Перечень материально-технического обеспечения для дисциплины</span>
      <p></p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-btn
        class="q-mb-md"
        label="Добавить МТО"
        color="secondary"
        @click="addMTO"
        v-show="!disabled"
      />
      <q-option-group
        :options="typeOptions"
        type="radio"
        v-model="searchType"
        inline
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
        <q-btn color="secondary" @click="searchOborud" label="Поиск"/>
      </div>
      <div class="row">
        <div class="col-5">
          <div class="text-h6">Выбранное МТО</div>
          <div v-for="item in oborudData" style="width: 95%">
            <q-field label="Название" stack-label filled class="q-mb-md">
              <template #control>
                <div class="text-subtitle1 self-center full-width no-outline">
                  <span>{{ item.name }} <q-chip v-if="item.inv" :label="`${item.inv}`"/> <q-chip v-if="item.caud__name"
                                                                                                 :label="`${item.caud__name}`"/></span>
                </div>
                <div class="q-gutter-x-md q-mt-md" v-show="!disabled">
                  <q-btn color="red" label="Удалить" @click="deleteOborud(item.id)"/>
                </div>
              </template>
            </q-field>
          </div>
        </div>
        <div class="col-7">
          <div v-for="item in searchData">
            <q-field label="Название" stack-label filled class="q-mb-md">
              <template #control>
                <div class="text-subtitle1 self-center full-width no-outline">
                  <span>{{ item.name }} <q-chip v-if="item.inv" :label="`${item.inv}`"/> <q-chip v-if="item.caud__name"
                                                                                                 :label="`${item.caud__name}`"/></span>
                </div>
                <div class="q-gutter-x-md q-mt-md">
                  <q-btn color="primary" label="Добавить" @click="addOborud(item)" :disable="checkTaken(item.id)"/>
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
