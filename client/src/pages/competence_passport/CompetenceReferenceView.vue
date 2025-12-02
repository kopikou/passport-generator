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
          style="min-width: 200px;"
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
      binary-state-sort
      flat
      bordered
    >
      <template v-slot:top>
        <div class="text-h6">Всего компетенций: {{ filteredCompetences.length }}</div>
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
        <q-td :props="props">
          {{ props.value }}
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
  { label: 'УК - Универсальные компетенции', value: 'УК' },
  { label: 'ОПК - Общепрофессиональные компетенции', value: 'ОПК' },
  { label: 'ПК - Профессиональные компетенции', value: 'ПК' }
]

const columns = [
  {
    name: 'competence_index',
    required: true,
    label: 'Индекс компетенции',
    align: 'left',
    field: row => row.competence_index,
    sortable: true
  },
  {
    name: 'competence',
    required: true,
    label: 'Содержание компетенции',
    align: 'left',
    field: row => row.competence,
    sortable: true
  },
  {
    name: 'type',
    label: 'Тип',
    align: 'center',
    field: row => getCompetenceType(row.competence_index),
    sortable: true
  }
]

const pagination = ref({
  sortBy: 'competence_index',
  descending: false,
  page: 1,
  rowsPerPage: 25
})

function getCompetenceType(competenceIndex) {
  if (!competenceIndex) return 'Не указан'
  
  if (competenceIndex.includes('УК')) return 'УК'
  if (competenceIndex.includes('ОПК')) return 'ОПК'
  if (competenceIndex.includes('ПК')) return 'ПК'
  
  return 'Другой'
}

function getTypeColor(type) {
  const colors = {
    'УК': 'blue',
    'ОПК': 'green',
    'ПК': 'orange',
    'Другой': 'grey'
  }
  return colors[type] || 'grey'
}

const filteredCompetences = computed(() => {
  let filtered = competences.value
  
  // Фильтр по типу компетенции
  if (competenceTypeFilter.value) {
    filtered = filtered.filter(comp => 
      getCompetenceType(comp.competence_index) === competenceTypeFilter.value.value
    )
  }
  
  // Поиск по тексту
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
    console.error('Error loading competences:', error)
  } finally {
    loading.value = false
  }
}

watch(() => store.currentPlanId, (newPlanId) => {
  if (newPlanId) {
    loadCompetences()
  }
})

onMounted(() => {
  loadCompetences()
})
</script>