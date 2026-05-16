<script setup lang="ts">
import { ref, computed, onBeforeMount} from 'vue'
import { useCompetencePassportStore } from 'src/stores/competencePassportStore'
import { storeToRefs } from 'pinia'

const store = useCompetencePassportStore()
const {
  currentPlanId,
  competences: storeCompetences,
  loading
} = storeToRefs(store)

const competenceTypeFilter = ref<string | null>(null)
const searchFilter = ref('')

const competenceTypeOptions = [
  { label: 'Универсальные компетенции', value: 'Универсальная' },
  { label: 'Общепрофессиональные компетенции', value: 'Общепрофессиональная' },
  { label: 'Профессиональные компетенции', value: 'Профессиональная' },
  { label: 'Дополнительные компетенции', value: 'Дополнительная' }
]

const columns = [
  {
    name: 'competence_index',
    required: true,
    label: 'Индекс компетенции',
    align: 'left',
    field: (row: any) => row.competence_index,
    sortable: true
  },
  {
    name: 'competence',
    required: true,
    label: 'Содержание компетенции',
    align: 'left',
    field: (row: any) => row.competence,
    sortable: true
  },
  {
    name: 'type',
    label: 'Тип',
    align: 'center',
    field: (row: any) => row.type,
    sortable: true
  }
]

const pagination = ref({
  page: 1,
  rowsPerPage: 0 
})

// Фильтрация
const filteredCompetences = computed(() => {
  let result = storeCompetences.value

  if (competenceTypeFilter.value) {
    result = result.filter(comp => comp.type === competenceTypeFilter.value)
  }

  if (searchFilter.value) {
    const term = searchFilter.value.toLowerCase().trim()
    result = result.filter(comp =>
      comp.competence_index.toLowerCase().includes(term) ||
      comp.competence.toLowerCase().includes(term)
    )
  }

  return result
})

const noDataMessage = computed(() => {
  if (storeCompetences.value.length === 0) {
    return 'Нет данных о компетенциях'
  }
  if (filteredCompetences.value.length === 0) {
    return 'Нет компетенций, соответствующих фильтрам'
  }
  return 'Нет данных'
})

// Цвета для типов
const getTypeColor = (type) => {
  const colors: Record<string, string> = {
    'Универсальная': 'blue',
    'Общепрофессиональная': 'green',
    'Профессиональная': 'orange',
    'Дополнительная': 'purple'
  }
  return colors[type] || 'grey'
}

async function loadReferences() {
  await store.fetchReferences(currentPlanId.value)
}

onBeforeMount(() => {
  if (currentPlanId.value) loadReferences()
})
</script>

<template>
  <div class="q-mb-lg q-pa-sm">
    <div class="row items-center q-col-gutter-md q-mb-md">
      <div class="col-12 col-md">
        <h2 class="text-h4 q-ma-none">Компетенции</h2>
        <div class="text-subtitle1 text-grey">
          Справочник всех компетенций
        </div>
      </div>
      <div class="col-12 col-sm-auto q-mr-md">
        <q-select
          v-model="competenceTypeFilter"
          :options="competenceTypeOptions"
          label="Фильтр по типам"
          option-value="value"
          emit-value
          dense
          outlined
          clearable
          style="min-width: 220px;"
        />
      </div>
      <div class="col-12 col-sm-auto">
        <q-input
          v-model="searchFilter"
          placeholder="Поиск по компетенциям..."
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
      :rows="filteredCompetences"
      :columns="columns"
      row-key="competence_index"
      :loading="loading"
      :pagination="pagination"
      flat
      bordered
      :no-data-label="noDataMessage"
    >
      <template v-slot:top>
        <div class="text-h6">
          Всего компетенций: {{ filteredCompetences.length }}
          <template v-if="filteredCompetences.length !== storeCompetences.length">
            (отфильтровано из {{ storeCompetences.length }})
          </template>
        </div>
        <q-space />
      </template>

      <template v-slot:body-cell-competence_index="props">
        <q-td :props="props">
          <div class="text-weight-bold text-primary">
            {{ props.value }}
          </div>
        </q-td>
      </template>

      <template v-slot:body-cell-competence="props">
        <q-td :props="props" class="competence-content-cell">
          <div class="competence-text">
            {{ props.value }}
          </div>
        </q-td>
      </template>

      <template v-slot:body-cell-type="props">
        <q-td :props="props">
          <q-badge :color="getTypeColor(props.value)" class="q-px-sm q-py-xs">
            {{ props.value }}
          </q-badge>
        </q-td>
      </template>
    </q-table>
  </div>
</template>

<style scoped>
.competence-text {
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