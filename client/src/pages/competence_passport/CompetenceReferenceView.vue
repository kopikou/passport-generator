<template>
  <div class="q-pa-md">
    <div class="row items-center q-mb-md">
      <div class="col">
        <h2 class="text-h4 q-ma-none">Компетенции</h2>
        <div class="text-subtitle1 text-grey">
          Справочник всех компетенций 
        </div>
      </div>
      <div class="col-auto q-mr-md">
        <q-select
          v-model="competenceTypeFilter"
          :options="competenceTypeOptions"
          label="Фильтр по типам"
          dense
          outlined
          clearable
          style="min-width: 220px;"
        />
      </div>
      <div class="col-auto">
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
      row-key="id"
      :loading="loading"
      :pagination="pagination"
      flat
      bordered
      :no-data-label="noDataMessage"
    >
      <template v-slot:top>
        <div class="text-h6">
          Всего компетенций: {{ filteredCompetences.length }}
          <template v-if="filteredCompetences.length !== competences.length">
            (отфильтровано из {{ competences.length }})
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

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useCompetencePassportStore } from 'stores/competencePassportStore'

const store = useCompetencePassportStore()
const loading = ref(false)
const competences = ref([])
const competenceTypeFilter = ref(null)
const searchFilter = ref('')
const currentPlan = ref(null)

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
    field: row => row.competence_index,
    style: 'width: 150px; min-width: 150px;'
  },
  {
    name: 'competence',
    required: true,
    label: 'Содержание компетенции',
    align: 'left',
    field: row => row.competence,
    style: 'min-width: 800px;'
  },
  {
    name: 'type',
    label: 'Тип',
    align: 'center',
    field: row => getCompetenceType(row.competence_index),
    style: 'width: 180px; min-width: 180px;'
  }
]

const pagination = ref({
  page: 1,
  rowsPerPage: 0
})

const noDataMessage = computed(() => {
  if (competences.value.length === 0) {
    return 'Нет данных о компетенциях'
  }
  if (filteredCompetences.value.length === 0) {
    return 'Нет компетенций, соответствующих фильтрам'
  }
  return 'Нет данных'
})

function getCompetenceType(competenceIndex) {
  if (!competenceIndex) return 'Неизвестно'
  
  if (competenceIndex.includes('УК') || competenceIndex.startsWith('УК')) {
    return 'Универсальная'
  }
  if (competenceIndex.includes('ОПК') || competenceIndex.startsWith('ОПК')) {
    return 'Общепрофессиональная'
  }
  if (competenceIndex.includes('ПК') || competenceIndex.startsWith('ПК')) {
    return 'Профессиональная'
  }
  if (competenceIndex.includes('ДК') || competenceIndex.startsWith('ДК')) {
    return 'Дополнительная'
  }
  
  return 'Другая'
}

function getTypeColor(type) {
  const colors = {
    'Универсальная': 'blue',
    'Общепрофессиональная': 'green',
    'Профессиональная': 'orange',
    'Дополнительная': 'purple',
    'Другая': 'grey'
  }
  return colors[type] || 'grey'
}

const filteredCompetences = computed(() => {
  let filtered = competences.value
  
  if (competenceTypeFilter.value) {
    filtered = filtered.filter(comp => 
      getCompetenceType(comp.competence_index) === competenceTypeFilter.value.value
    )
  }
  
  if (searchFilter.value) {
    const searchLower = searchFilter.value.toLowerCase()
    filtered = filtered.filter(comp => 
      comp.competence_index.toLowerCase().includes(searchLower) ||
      comp.competence.toLowerCase().includes(searchLower)
    )
  }
  
  return filtered
})

async function loadCompetences() {
  loading.value = true
  try {
    const planId = store.currentPlanId
    
    if (!planId) {
      throw new Error('Plan ID is not available. Please select a plan first.')
    }
    
    const response = await store.fetchAllCompetences(planId)
    
    competences.value = response.competences || []
    currentPlan.value = {
      planname: response.plan_name,
      abbrprofile: response.abbrprofile
    }
    
    
  } catch (error) {
    competences.value = []
    currentPlan.value = null
  } finally {
    loading.value = false
  }
}

watch(() => store.currentPlanId, (newPlanId) => {
  if (newPlanId) {
    loadCompetences()
  } else {
    competences.value = []
    currentPlan.value = null
  }
})

onMounted(() => {
  if (store.currentPlanId) {
    loadCompetences()
  }
})
</script>

<style scoped>
.text-subtitle1 {
  margin-bottom: 1rem;
}

.q-table {
  margin-top: 1rem;
}

.text-weight-bold {
  font-weight: 600;
}

.competence-content-cell {
  max-width: 800px;
}

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
}

:deep(.q-table__card) {
  overflow-x: auto;
}
</style>