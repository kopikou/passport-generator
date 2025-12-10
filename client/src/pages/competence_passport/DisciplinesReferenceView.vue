<template>
  <div class="q-pa-md">
    <div class="row items-center q-mb-md">
      <div class="col">
        <h2 class="text-h4 q-ma-none">Дисциплины</h2>
        <div class="text-subtitle1 text-grey">
          Справочник всех дисциплин
        </div>
      </div>
      <div class="col-auto q-mr-md">
        <q-select
          v-model="selectedTypes"
          :options="disciplineTypeOptions"
          label="Фильтр по типам"
          dense
          outlined
          clearable
          multiple
          style="min-width: 250px;"
          emit-value
          map-options
        />
      </div>
      <div class="col-auto">
        <q-input
          v-model="searchFilter"
          placeholder="Поиск по дисциплинам..."
          dense
          outlined
          clearable
        >
          <template v-slot:append>
            <q-icon name="search" />
          </template>
        </q-input>
      </div>
    </div>

    <q-table
      :rows="filteredDisciplines"
      :columns="columns"
      row-key="id"
      :loading="loading"
      :pagination="pagination"
      binary-state-sort
      flat
      bordered
    >
      <template v-slot:top>
        <div class="text-h6">Всего дисциплин: {{ filteredDisciplines.length }}</div>
        <q-space />
        <div class="text-caption text-grey" v-if="selectedTypes && selectedTypes.length > 0">
          Отфильтровано по типам: {{ selectedTypes.join(', ') }}
        </div>
      </template>

      <template v-slot:body-cell-newdisid="props">
        <q-td :props="props">
          <div class="text-weight-medium text-primary">
            {{ props.value }}
          </div>
        </q-td>
      </template>

      <template v-slot:body-cell-dis="props">
        <q-td :props="props">
          {{ props.value }}
        </q-td>
      </template>

      <template v-slot:body-cell-types="props">
        <q-td :props="props">
          <div class="column q-gap-y-sm" style="min-height: 60px; padding: 8px 0; align-items: center;">
            <q-badge 
              v-for="type in props.value" 
              :key="type"
              :color="getTypeColor(type)" 
              class="q-px-sm q-py-xs"
              style="width: fit-content; margin-bottom: 4px;"
            >
              {{ type }}
            </q-badge>
          </div>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useCompetencePassportStore } from 'stores/competencePassportStore'

const store = useCompetencePassportStore()
const loading = ref(false)
const disciplines = ref([])
const searchFilter = ref('')
const selectedTypes = ref([]) 
const currentPlan = ref(null)

// Определяем группы, которые нужно исключить
const groupsToExclude = [
  'Б1',
  'Б1.Б',
  'Б1.Б.01',
  'Б1.Б.02',
  'Б1.Б.03',
  'Б1.Б.04',
  'Б1.Б.05',
  'Б1.В',
  'Б1.В.01',
  'Б1.В.02',
  'Б1.В.03',
  'Б2',
  'Б2.Б',
  'Б2.В',
  'Б3',
  'ФТД'
]

// Функция для проверки, является ли индекс обобщающей группой
function isExcludedGroup(disciplineIndex) {
  if (!disciplineIndex) return false
  
  return groupsToExclude.some(group => disciplineIndex === group)
}

// Цветовая схема для всех типов
const typeColors = {
  'Обязательная часть': 'blue',
  'Общеобразовательный модуль': 'indigo',
  'Фундаментальный модуль': 'cyan', 
  'Базовый модуль направления': 'teal',
  'Модуль проектной деятельности': 'green',
  'Модуль по физической культуре': 'light-green',
  'Вариативная часть': 'orange',
  'Модуль профильной подготовки': 'deep-orange',
  'Модуль дополнительного профиля': 'brown',
  'Практика': 'purple',
  'ГИА': 'red',
  'Другой': 'grey'
}

const disciplineTypeOptions = Object.keys(typeColors).map(type => ({
  label: type,
  value: type
}))

const columns = [
  {
    name: 'newdisid',
    required: true,
    label: 'Индекс дисциплины',
    align: 'left',
    field: row => row.newdisid,
    sortable: true
  },
  {
    name: 'dis',
    required: true,
    label: 'Наименование дисциплины',
    align: 'left',
    field: row => row.dis,
    sortable: true
  },
  {
    name: 'types',
    label: 'Типы дисциплины',
    align: 'center',
    field: row => getDisciplineTypes(row.newdisid),
    sortable: true
  }
]

const pagination = ref({
  sortBy: 'newdisid',
  descending: false,
  page: 1,
  rowsPerPage: 25
})

// Определяем все возможные типы дисциплины по индексу
function getDisciplineTypes(disciplineIndex) {
  if (!disciplineIndex) return ['Не указан']
  
  if (isExcludedGroup(disciplineIndex)) {
    return ['Обобщающая группа']
  }
  
  const types = []
  
  // Основные категории
  if (disciplineIndex.includes('Б1.Б')) types.push('Обязательная часть')
  if (disciplineIndex.includes('Б1.В')) types.push('Вариативная часть')
  if (disciplineIndex.includes('Б2')) types.push('Практика')
  if (disciplineIndex.includes('Б3')) types.push('ГИА')
  
  // Конкретные модули
  if (disciplineIndex.includes('Б1.Б.01')) types.push('Общеобразовательный модуль')
  if (disciplineIndex.includes('Б1.Б.02')) types.push('Фундаментальный модуль')
  if (disciplineIndex.includes('Б1.Б.03')) types.push('Базовый модуль направления')
  if (disciplineIndex.includes('Б1.Б.04')) types.push('Модуль проектной деятельности')
  if (disciplineIndex.includes('Б1.Б.05')) types.push('Модуль по физической культуре')
  if (disciplineIndex.includes('Б1.В.01')) types.push('Модуль проектной деятельности')
  if (disciplineIndex.includes('Б1.В.02')) types.push('Модуль профильной подготовки')
  if (disciplineIndex.includes('Б1.В.03')) types.push('Модуль дополнительного профиля')
  
  if (types.length === 0 && (disciplineIndex.includes('Б1.Б') || disciplineIndex.includes('Б1.В'))) {
    types.push('Другой')
  }
  
  return types.length > 0 ? types : ['Другой']
}

function getTypeColor(type) {
  return typeColors[type] || 'grey'
}

const filteredDisciplines = computed(() => {
  let filtered = disciplines.value
  
  filtered = filtered.filter(disc => !isExcludedGroup(disc.newdisid))
  
  // Фильтр по поисковому запросу
  if (searchFilter.value) {
    const searchLower = searchFilter.value.toLowerCase()
    filtered = filtered.filter(disc => 
      disc.dis.toLowerCase().includes(searchLower) ||
      (disc.newdisid && disc.newdisid.toLowerCase().includes(searchLower))
    )
  }
  
  if (selectedTypes.value && selectedTypes.value.length > 0) {
    filtered = filtered.filter(disc => {
      const discTypes = getDisciplineTypes(disc.newdisid)
      // Исключаем обобщающие группы из фильтрации по типам
      if (discTypes.includes('Обобщающая группа')) return false
      return selectedTypes.value.some(selectedType => 
        discTypes.includes(selectedType)
      )
    })
  }
  
  return filtered
})

async function loadDisciplines() {
  loading.value = true
  try {
    const planId = store.currentPlanId
    
    if (!planId) {
      throw new Error('Plan ID is not available. Please select a plan first.')
    }
    
    const response = await store.fetchAllDisciplines(planId)
    disciplines.value = response.disciplines || []
    currentPlan.value = {
      planname: response.plan_name,
      abbrprofile: response.abbrprofile
    }
    
  } catch (error) {
    console.error('Error loading disciplines:', error)
  } finally {
    loading.value = false
  }
}

watch(() => store.currentPlanId, (newPlanId) => {
  if (newPlanId) {
    loadDisciplines()
  }
})

onMounted(() => {
  loadDisciplines()
})
</script>