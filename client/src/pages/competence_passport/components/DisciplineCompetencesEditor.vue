<template>
  <q-dialog v-model="showDialog" persistent maximized>
    <q-card class="full-height-dialog">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">Управление компетенциями дисциплины</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>

      <q-card-section class="q-pt-none">
        <!-- Информация о дисциплине -->
        <div class="row items-center q-mb-sm">
          <div class="col">
            <div class="text-subtitle1">
              <strong>Дисциплина:</strong> {{ discipline?.index }} - {{ discipline?.name }}
            </div>
            <div class="text-caption text-blue q-mt-xs">
              <q-icon name="info" />
              Установите флаги для компетенций, которые формируются данной дисциплиной
            </div>
          </div>
          
          <!-- Статистика -->
          <div class="col-auto">
            <div class="row items-center q-gutter-md">
              <q-badge color="grey" outline>
                Всего: {{ allCompetences.length }}
              </q-badge>
              <q-badge color="positive" outline>
                Выбрано: {{ selectedCount }}
              </q-badge>
              <q-badge color="negative" outline>
                Не выбрано: {{ unselectedCount }}
              </q-badge>
            </div>
          </div>
        </div>
        
        <!-- Панель фильтров -->
        <div class="row q-mb-md q-gutter-sm">
          <div class="col">
            <q-input
              v-model="searchQuery"
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
          
          <div class="col-auto">
            <q-select
              v-model="selectedTypeFilter"
              :options="typeOptions"
              label="Тип компетенции"
              dense
              outlined
              clearable
              emit-value
              map-options
              style="min-width: 200px;"
            />
          </div>
          
          <div class="col-auto">
            <q-select
              v-model="selectedStatusFilter"
              :options="statusOptions"
              label="Статус"
              dense
              outlined
              clearable
              emit-value
              map-options
              style="min-width: 150px;"
            />
          </div>
          
          <div class="col-auto">
            <q-btn
              flat
              dense
              color="positive"
              icon="check_box"
              label="Все"
              @click="selectAll"
              :disabled="loading"
            />
            <q-btn
              flat
              dense
              color="negative"
              icon="check_box_outline_blank"
              label="Ничего"
              @click="unselectAll"
              :disabled="loading"
            />
            <q-btn
              flat
              dense
              color="primary"
              icon="filter_alt_off"
              @click="resetFilters"
              :disabled="loading"
            >
              <q-tooltip>Сбросить фильтры</q-tooltip>
            </q-btn>
          </div>
        </div>
        
        <div v-if="!loading" class="competence-table-container">
          <q-table
            :rows="filteredCompetences"
            :columns="columns"
            row-key="competence_index"
            :loading="saving"
            :pagination="pagination"
            :rows-per-page-options="[20, 50, 100, 200]"
            flat
            bordered
            class="full-height-table"
            virtual-scroll
            :no-data-label="noDataMessage"
          >
            <template v-slot:top>
              <div class="text-h6">
                Компетенции плана ({{ filteredCompetences.length }} из {{ allCompetences.length }})
                <template v-if="filteredCompetences.length !== allCompetences.length">
                  (отфильтровано)
                </template>
              </div>
              <q-space />
              <div class="text-caption text-grey" v-if="searchQuery">
                Поиск: "{{ searchQuery }}"
              </div>
            </template>

            <template v-slot:body="props">
              <q-tr :props="props">
                <!-- Флаг применения -->
                <q-td key="selected" :props="props">
                  <div class="text-center">
                    <q-toggle
                      v-model="props.row.selected"
                      color="positive"
                      size="lg"
                      :disable="saving"
                      @update:model-value="onToggleCompetence(props.row)"
                    />
                  </div>
                </q-td>
                
                <!-- Индекс компетенции -->
                <q-td key="competence_index" :props="props">
                  <div class="text-weight-medium">
                    <q-badge :color="getTypeColor(props.row.type)" class="q-mr-sm">
                      {{ props.row.type_short }}
                    </q-badge>
                    {{ props.row.competence_index }}
                  </div>
                  <div class="text-caption text-grey">
                    Индикаторов: {{ props.row.indicators_count || 0 }}
                  </div>
                </q-td>
                
                <!-- Содержание компетенции -->
                <q-td key="competence" :props="props">
                  <div class="text-body2">{{ props.row.competence }}</div>
                  <div v-if="props.row.indicators && props.row.indicators.length > 0" class="q-mt-xs">
                    <div class="text-caption text-grey">Индикаторы:</div>
                    <div class="text-caption">
                      <q-chip
                        v-for="indicator in props.row.indicators"
                        :key="indicator.index"
                        size="sm"
                        color="blue-grey-1"
                        text-color="grey-8"
                        class="q-mx-xs"
                      >
                        {{ indicator.index }}
                      </q-chip>
                    </div>
                  </div>
                </q-td>
              </q-tr>
            </template>
          </q-table>
          
          <div class="text-caption text-grey q-mt-sm">
            <q-icon name="info" />
            <template v-if="filteredCompetences.length === allCompetences.length">
              Все компетенции плана ({{ allCompetences.length }})
            </template>
            <template v-else>
              Найдено: {{ filteredCompetences.length }} из {{ allCompetences.length }}
            </template>
          </div>
        </div>
      </q-card-section>

      <q-card-actions align="right" class="q-pa-md bg-grey-2">
        <q-btn 
          flat 
          label="Закрыть" 
          color="negative" 
          v-close-popup 
          :disabled="saving"
        />
        <q-btn 
          label="Сохранить" 
          color="positive" 
          @click="saveChanges"
          :loading="saving"
          :disabled="saving || !hasChanges"
        >
          <q-tooltip v-if="!hasChanges">
            Нет изменений для сохранения
          </q-tooltip>
        </q-btn>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useCompetencePassportStore } from 'stores/competencePassportStore'
import { storeToRefs } from 'pinia'
import { useQuasar } from 'quasar'

const props = defineProps({
  planId: {
    type: Number,
    required: true
  },
  disciplineId: {
    type: Number,
    required: true
  },
  disciplineIndex: {
    type: String,
    required: true
  },
  disciplineName: {
    type: String,
    required: true
  },
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:show', 'saved'])

const $q = useQuasar()
const store = useCompetencePassportStore()
const {
  saving,
  currentPlanId,
  loading
} = storeToRefs(store)

const showDialog = ref(false)
const showDetailsDialog = ref(false)
const selectedCompetence = ref(null)

const searchQuery = ref('')
const selectedTypeFilter = ref(null)
const selectedStatusFilter = ref(null)

const discipline = ref(null)
const allCompetences = ref([])
const originalCompetences = ref([])

const noDataMessage = computed(() => {
  if (allCompetences.value.length === 0) {
    return 'Нет данных о компетенциях'
  }
  if (filteredCompetences.value.length === 0) {
    return 'Нет компетенций, соответствующих фильтрам'
  }
  return 'Нет данных'
})

const typeOptions = computed(() => {
  const types = new Set(allCompetences.value.map(c => c.type))
  return Array.from(types).map(type => ({
    label: type,
    value: type
  })).sort((a, b) => a.label.localeCompare(b.label))
})

const statusOptions = [
  { label: 'Выбранные', value: 'selected' },
  { label: 'Не выбранные', value: 'unselected' }
]

// Статистика
const selectedCount = computed(() => {
  return allCompetences.value.filter(c => c.selected).length
})

const unselectedCount = computed(() => {
  return allCompetences.value.filter(c => !c.selected).length
})

const hasChanges = computed(() => {
  if (!originalCompetences.value.length || !allCompetences.value.length) return false
  
  const originalSelected = originalCompetences.value
    .filter(c => c.selected)
    .map(c => c.competence_index)
    .sort()
  
  const currentSelected = allCompetences.value
    .filter(c => c.selected)
    .map(c => c.competence_index)
    .sort()
  
  return JSON.stringify(originalSelected) !== JSON.stringify(currentSelected)
})

// Компетенции с фильтрацией
const filteredCompetences = computed(() => {
  let filtered = allCompetences.value
  
  // Фильтр по поисковому запросу
  if (searchQuery.value) {
    const searchLower = searchQuery.value.toLowerCase()
    filtered = filtered.filter(comp => 
      comp.competence_index.toLowerCase().includes(searchLower) ||
      comp.competence.toLowerCase().includes(searchLower)
    )
  }
  
  // Фильтр по типу
  if (selectedTypeFilter.value) {
    filtered = filtered.filter(comp => comp.type === selectedTypeFilter.value)
  }
  
  // Фильтр по статусу
  if (selectedStatusFilter.value === 'selected') {
    filtered = filtered.filter(comp => comp.selected)
  } else if (selectedStatusFilter.value === 'unselected') {
    filtered = filtered.filter(comp => !comp.selected)
  }
  
  return filtered
})

// Колонки таблицы
const columns = [
  {
    name: 'selected',
    label: 'Формируется',
    align: 'center',
    field: row => row.selected,
    style: 'width: 100px;'
  },
  {
    name: 'competence_index',
    label: 'Индекс компетенции',
    align: 'left',
    field: row => row.competence_index,
    style: 'width: 150px;'
  },
  {
    name: 'competence',
    label: 'Содержание компетенции',
    align: 'left',
    field: row => row.competence,
    style: 'min-width: 400px;'
  },
]

const pagination = ref({
  page: 1,
  rowsPerPage: 0
})

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

function getShortType(type) {
  const shorts = {
    'Универсальная': 'УК',
    'Общепрофессиональная': 'ОПК',
    'Профессиональная': 'ПК',
    'Дополнительная': 'ДК',
    'Другая': 'Др'
  }
  return shorts[type] || 'Др'
}

async function loadCompetenceData() {
  loading.value = true
  try {
    const response = await store.fetchDisciplineCompetencesDetailed(props.planId, props.disciplineId)
    
    allCompetences.value = response.competences.map(comp => ({
      ...comp,
      type_short: getShortType(comp.type),
      indicators: comp.indicators || [],
      indicators_count: comp.indicators_count || 0
    }))

    originalCompetences.value = JSON.parse(JSON.stringify(allCompetences.value))
    
    discipline.value = {
      id: props.disciplineId,
      index: props.disciplineIndex,
      name: props.disciplineName,
      planId: props.planId
    }
    
  } catch (error) {
    console.error('Error loading competence data:', error)
    $q.notify({
      type: 'negative',
      message: `Ошибка загрузки данных: ${error.message}`,
      position: 'top-right'
    })
  } finally {
    loading.value = false
  }
}

function onToggleCompetence(competence) {
  if (competence.selected) {
    if (!competence.indicators || competence.indicators.length === 0) {
      competence.indicators = [
        { index: `${competence.competence_index}.1`, name: '' }
      ]
      competence.indicators_count = 1
    }
  } else {
    competence.indicators = []
    competence.indicators_count = 0
  }
}

function selectAll() {
  allCompetences.value.forEach(comp => {
    comp.selected = true
    if (!comp.indicators || comp.indicators.length === 0) {
      comp.indicators = [{ index: `${comp.competence_index}.1`, name: '' }]
      comp.indicators_count = 1
    }
  })
}

function unselectAll() {
  allCompetences.value.forEach(comp => {
    comp.selected = false
    comp.indicators = []
    comp.indicators_count = 0
  })
}

function resetFilters() {
  searchQuery.value = ''
  selectedTypeFilter.value = null
  selectedStatusFilter.value = null
}

async function saveChanges() {
  if (!hasChanges.value) {
    $q.notify({
      type: 'info',
      message: 'Нет изменений для сохранения',
      position: 'top-right',
      timeout: 2000
    })
    return
  }

  saving.value = true
  try {
    const selectedCompetencesData = allCompetences.value
      .filter(comp => comp.selected)
      .map(comp => ({
        competence_index: comp.competence_index,
        competence: comp.competence,
        indicators: comp.indicators || []
      }))
    
    await store.updateDisciplineCompetences(selectedCompetencesData)
    
    $q.notify({
      type: 'positive',
      message: `Успешно сохранено ${selectedCompetencesData.length} компетенций`,
      position: 'top-right',
      timeout: 3000
    })
    
    originalCompetences.value = JSON.parse(JSON.stringify(allCompetences.value))
    
    emit('saved')
    showDialog.value = false
    
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: `Ошибка при сохранении: ${error.response?.data?.error || error.message}`,
      position: 'top-right'
    })
  } finally {
    saving.value = false
  }
}

watch(() => props.show, (newVal) => {
  showDialog.value = newVal
  if (newVal) {
    resetFilters()
    loadCompetenceData()
  } else {
    discipline.value = null
    allCompetences.value = []
    originalCompetences.value = []
    selectedCompetence.value = null
    showDetailsDialog.value = false
  }
}, { immediate: true })

watch(showDialog, (newVal) => {
  if (!newVal) {
    emit('update:show', false)
  }
})
</script>

<style scoped lang="scss">
.full-height-dialog {
  width: 90vw;
  max-width: 1200px;
  height: 90vh;
  
  .q-card__section {
    padding: 16px;
  }
}

.competence-table-container {
  height: calc(90vh - 280px); 
  min-height: 400px;
  display: flex;
  flex-direction: column;
  
  .full-height-table {
    flex: 1;
    min-height: 0; 
    
    :deep(.q-table__container) {
      height: 100%;
      
      .q-table__middle {
        flex: 1;
        min-height: 0;
      }
    }
  }
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>