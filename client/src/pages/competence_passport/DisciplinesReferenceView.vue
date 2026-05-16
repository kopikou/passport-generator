<script setup lang="ts">
import { ref, computed, onBeforeMount } from 'vue'
import { useCompetencePassportStore } from 'src/stores/competencePassportStore'
import { storeToRefs } from 'pinia'

const store = useCompetencePassportStore()
const {
  currentPlanId,
  disciplines: storeDisciplines,
  loading
} = storeToRefs(store)

const searchFilter = ref('')
const selectedTypes = ref<string[]>([])

// Цвета типов
const typeColors: Record<string, string> = {
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
    name: 'discipline_index',
    required: true,
    label: 'Индекс дисциплины',
    align: 'left',
    field: (row: any) => row.discipline_index,
    sortable: true
  },
  {
    name: 'discipline_name',
    required: true,
    label: 'Наименование дисциплины',
    align: 'left',
    field: (row: any) => row.discipline_name,
    sortable: true
  },
  {
    name: 'types',
    label: 'Типы дисциплины',
    align: 'center',
    field: (row: any) => row.type,
    sortable: false
  }
]

const pagination = ref({
  page: 1,
  rowsPerPage: 0
})

// Фильтрация
const filteredDisciplines = computed(() => {
  let result = storeDisciplines.value

  // Поиск
  if (searchFilter.value) {
    const term = searchFilter.value.toLowerCase().trim()
    result = result.filter(disc =>
      disc.discipline_index.toLowerCase().includes(term) ||
      disc.discipline_name.toLowerCase().includes(term)
    )
  }

  // Фильтр по типам
  const types = selectedTypes.value || []
  if (types.length > 0) {
    result = result.filter(disc =>
      types.some(type => disc.type.includes(type))
    )
  }

  return result
})

const hasSelectedTypes = computed(() => {
  return (selectedTypes.value || []).length > 0
})

const getTypeColor = (type) => {
  return typeColors[type] || 'grey'
}

</script>

<template>
  <div class="q-mb-lg q-pa-sm">
    <div class="row items-center q-col-gutter-md q-mb-md">
      <div class="col-12 col-md">
        <h2 class="text-h4 q-ma-none">Дисциплины</h2>
        <div class="text-subtitle1 text-grey">
          Справочник всех дисциплин
        </div>
      </div>
      <div class="col-12 col-sm-auto q-mr-md">
        <q-select
          v-model="selectedTypes"
          :options="disciplineTypeOptions"
          label="Фильтр по типам"
          dense
          outlined
          clearable
          multiple
          style="min-width: 220px;"
          emit-value
          map-options
        />
      </div>
      <div class="col-12 col-sm-auto">
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
      row-key="discipline_id"
      :loading="loading"
      :pagination="pagination"
      binary-state-sort
      flat
      bordered
    >
      <template v-slot:top>
        <div class="text-h6">
          Всего дисциплин: {{ filteredDisciplines.length }}
        </div>
        <q-space />
        <div
          v-if="hasSelectedTypes"
          class="text-caption text-grey"
        >
          Отфильтровано по типам: {{ selectedTypes.join(', ') }}
        </div>
      </template>

      <template v-slot:body-cell-discipline_index="props">
        <q-td :props="props">
          <div class="text-weight-medium text-primary">
            {{ props.value }}
          </div>
        </q-td>
      </template>

      <template v-slot:body-cell-discipline_name="props">
        <q-td :props="props">
          <div class="discipline-name">
            {{ props.value }}
          </div>
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

<style scoped>
.q-table {
  margin-top: 1rem;
}

.discipline-name {
  word-wrap: break-word;
  white-space: normal;
  line-height: 1.4; 
}

:deep(.q-table) {
  table-layout: fixed;
}

:deep(.q-table th),
:deep(.q-table td) {
  vertical-align: top;
  white-space: normal;
}
</style>