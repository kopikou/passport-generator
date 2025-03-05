<script setup lang="ts">

import {useRouter} from "vue-router";
import {onBeforeMount, ref, watch} from "vue";
import {useQuasar} from "quasar";
import {api} from "boot/axios";
import _ from "lodash";

const props = defineProps({
  id: {
    required: true,
    type: Number,
  }
})

const router = useRouter()
const $q = useQuasar()

const step = ref(0)

// const columns = [
//   {
//     name: 'ckaf',
//     field: 'ckaf',
//     label: 'Кафедра',
//     align: 'center',
//   },
//   {
//     name: 'name',
//     field: 'name',
//     label: 'Наименование ООП',
//     align: 'center',
//   },
//   {
//     name: 'cfac',
//     field: 'cfac',
//     label: 'Институт',
//     align: 'center',
//   },
//   {
//     name: 'range',
//     field: 'range',
//     label: 'Срок освоения',
//     align: 'center',
//   },
//   {
//     name: 'cfob',
//     field: 'cfob',
//     label: 'Форма обучения',
//     align: 'center',
//   },
//   {
//     name: 'startyear',
//     field: 'startyear',
//     label: 'Год начала обучения',
//     align: 'center',
//   },
//   {
//     name: 'fgt',
//     field: 'fgt',
//     label: 'ФГТ',
//     align: 'center',
//   },
//   {
//     name: 'viceRector',
//     field: 'viceRector',
//     label: 'Проректор по учебной работе',
//     align: 'center',
//   },
//   {
//     name: 'director',
//     field: 'director',
//     label: 'Директор института',
//     align: 'center',
//   },
//   {
//     name: 'zavkaf',
//     field: 'zavkaf',
//     label: 'Заведующий кафедрой',
//     align: 'center',
//   },
//   {
//     name: 'rop',
//     field: 'rop',
//     label: 'Руководитель ООП',
//     align: 'center',
//   },
//   {
//     name: 'year',
//     field: 'year',
//     label: 'Год',
//     align: 'center',
//   },
// ]

const columnsNames = {
  'ckaf': {label: 'Кафедра', visible: true},
  'name': {label: 'Наименование ООП', visible: true},
  'cfac': {label: 'Институт', visible: true},
  'rng': {label: 'Срок освоения', visible: true},
  'cfob': {label: 'Форма обучения', visible: true},
  'startyear': {label: 'Год начала обучения', visible: true},
  'fgt': {label: 'ФГТ', visible: true},
  'viceRector': {label: 'Проректор по учебной работе', visible: true},
  'director': {label: 'Директор института', visible: true},
  'zavkaf': {label: 'Заведующий кафедрой', visible: true},
  'rop': {label: 'Руководитель ООП', visible: true},
  'year': {label: 'Год', visible: true},
  'id': {label: 'Идентификатор', visible: false},
  'mira_id': {label: 'Идентификатор в mira', visible: false},
}

const columns = [
  {
    name: 'label',
    field: 'label',
    label: 'Параметр',
    align: 'center',
  },
  {
    name: 'val',
    field: 'val',
    label: 'Значение',
    align: 'center',
  },
]

const rows = ref([])
const mainInfo = ref()

async function fetchPlanData() {
  let r = await api.get(`/api/generator/${props.id}/get-asp-program-detail/`)
  mainInfo.value = _.get(r.data, '[0]')
  _.forEach(r.data[0], (x, key) => {
    if (columnsNames[key].visible) {
      rows.value.push({
        "key": key,
        "val": x,
        "label": columnsNames[key].label,
      })
    }
  })
}

async function saveMainInfo(data, key) {
  mainInfo.value[key] = data
  let r = await api.post(`/api/generator/${mainInfo.value.id}/save-asp-program-data/`, mainInfo.value)
}

onBeforeMount(async () => {
  $q.loading.show({message: "Загрузка данных"})
  await fetchPlanData()
  $q.loading.hide()
})

</script>

<template>
  <div class="q-pa-lg q-gutter-y-sm">
    <q-btn @click="router.push('/scientific-plan')" color="primary" icon="mdi-arrow-left" label="Назад, к списку"/>
    <q-stepper
      v-model="step"
      color="primary"
      animated
      header-nav
    >

      <q-step
        :name="0"
        title="Основная информация"
        icon=""
      >
        <q-table
          :columns="columns"
          :rows="rows"
          :rows-per-page-options="[0]"
          hide-header
          hide-bottom
        >

          <template #body-cell-val="props">
            <q-td :props="props">
              <q-popup-edit v-slot="scope" v-model="props.row.val" auto-save>
                <q-input v-model="scope.value" autofocus @focusout="scope.set" @keyup.enter="scope.set" :debounce="1000" @update:modelValue="saveMainInfo(scope.value, props.row.key)"/>
              </q-popup-edit>
              {{ props.row.val }}
            </q-td>
          </template>
        </q-table>
      </q-step>

      <q-step
        :name="1"
        title="Примерный план выполнения научного исследования"
      >
        2
      </q-step>

      <q-step
        :name="2"
        title="Примерный план подготовки диссертации"
      >
        3
      </q-step>

      <q-step
        :name="3"
        title="Примерный план подготовки публикаций"
      >
        4
      </q-step>

    </q-stepper>
  </div>
</template>

<style scoped>

</style>
