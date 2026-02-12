<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useCompetencePassportStore } from 'src/stores/competencePassportStore'
import { storeToRefs } from 'pinia'
import { useQuasar } from 'quasar'
import _ from 'lodash'

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
  competences: storeCompetences,
  matrix,
  saving,
  loading
} = storeToRefs(store)

const showDialog = ref(false)
const searchQuery = ref('')
const selectedTypeFilter = ref<string | null>(null)
const selectedStatusFilter = ref<string | null>(null)

const allCompetences = ref<any[]>([])
const originalCompetences = ref<any[]>([])

const noDataMessage = computed(() => {
  if (storeCompetences.value.length === 0) {
    return 'Нет данных о компетенциях'
  }
  if (filteredCompetences.value.length === 0) {
    return 'Нет компетенций, соответствующих фильтрам'
  }
  return 'Нет данных'
})

const typeOptions = computed(() => {
  const types = new Set(storeCompetences.value.map(c => c.type))
  return Array.from(types).map(type => ({
    label: type,
    value: type
  })).sort((a, b) => a.label.localeCompare(b.label))
})

const statusOptions = [
  { label: 'Выбранные', value: 'selected' },
  { label: 'Не выбранные', value: 'unselected' }
]

const selectedCount = computed(() => {
  return allCompetences.value.filter(c => c.selected).length
})

const unselectedCount = computed(() => {
  return allCompetences.value.filter(c => !c.selected).length
})

const hasChanges = computed(() => {
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

// Фильтрация
const filteredCompetences = computed(() => {
  let filtered = allCompetences.value
  
  if (searchQuery.value) {
    const term = searchQuery.value.toLowerCase().trim()
    filtered = filtered.filter(comp =>
      comp.competence_index.toLowerCase().includes(term) ||
      comp.competence.toLowerCase().includes(term)
    )
  }
  
  if (selectedTypeFilter.value) {
    filtered = filtered.filter(comp => comp.type === selectedTypeFilter.value)
  }
  
  if (selectedStatusFilter.value === 'selected') {
    filtered = filtered.filter(comp => comp.selected)
  } else if (selectedStatusFilter.value === 'unselected') {
    filtered = filtered.filter(comp => !comp.selected)
  }
  
  return filtered
})

const columns = [
  {
    name: 'selected',
    label: 'Формируется',
    align: 'center',
    field: (row: any) => row.selected,
    style: 'width: 100px;'
  },
  {
    name: 'competence_index',
    label: 'Индекс компетенции',
    align: 'left',
    field: (row: any) => row.competence_index,
    style: 'width: 150px;'
  },
  {
    name: 'competence',
    label: 'Содержание компетенции',
    align: 'left',
    field: (row: any) => row.competence,
    style: 'min-width: 400px;'
  }
]

const pagination = ref({
  page: 1,
  rowsPerPage: 0
})


function getTypeColor(type) {
  const colors: Record<string, string> = {
    'Универсальная': 'blue',
    'Общепрофессиональная': 'green',
    'Профессиональная': 'orange',
    'Дополнительная': 'purple'
  }
  return colors[type] || 'grey'
}

async function loadCompetenceData() {
  const matrixDiscipline = matrix.value.find(
    item => item.type === 'discipline' && item.discipline_id === props.disciplineId
  )
  
  const currentCompetenceIndices = new Set(
    matrixDiscipline?.competence_list?.map((c: any) => c.competence_index) || []
  )
  
  allCompetences.value = storeCompetences.value.map(comp => ({
    ...comp,
    selected: currentCompetenceIndices.has(comp.competence_index),
  }))
  
  originalCompetences.value = _.cloneDeep(allCompetences.value)
}

function selectAll() {
  allCompetences.value.forEach(comp => {
    comp.selected = true
  })
}

function unselectAll() {
  allCompetences.value.forEach(comp => {
    comp.selected = false
  })
}

function resetFilters() {
  searchQuery.value = ''
  selectedTypeFilter.value = null
  selectedStatusFilter.value = null
}

// Сохранение
async function saveChanges() {
  if (!hasChanges.value) {
    $q.notify({
      type: 'info',
      message: 'Нет изменений для сохранения',
      timeout: 2000
    })
    return
  }

  try {
    const selectedCompetences = allCompetences.value
      .filter(comp => comp.selected)
      .map(comp => ({
        competence_index: comp.competence_index,
        competence: comp.competence,
        type: comp.type
      }))
    
    await store.updateDisciplineCompetences(
      props.planId,
      props.disciplineId,
      selectedCompetences
    )
    
    $q.notify({
      type: 'positive',
      message: `Успешно сохранено ${selectedCompetences.length} компетенций`,
      position: 'top-right',
      timeout: 3000
    })
    
    originalCompetences.value = _.cloneDeep(allCompetences.value)
    emit('saved')
    showDialog.value = false
    
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при сохранении компетенций',
      position: 'top-right'
    })
  }
}

watch(() => props.show, (newVal) => {
  showDialog.value = newVal
  if (newVal) {
    resetFilters()
    loadCompetenceData()
  } else {
    allCompetences.value = []
    originalCompetences.value = []
  }
}, { immediate: true })

watch(showDialog, (newVal) => {
  if (!newVal) {
    emit('update:show', false)
  }
})
</script>

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
              <strong>Дисциплина:</strong> {{ props.disciplineIndex }} - {{ props.disciplineName }}
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
                    />
                  </div>
                </q-td>
                
                <!-- Индекс компетенции -->
                <q-td key="competence_index" :props="props" class="competence-index-cell">
                  <q-badge :color="getTypeColor(props.row.type)" class="q-mr-sm">
                    {{ props.row.competence_index }}
                  </q-badge>
                </q-td>
                
                <!-- Содержание компетенции -->
                <q-td key="competence" :props="props" class="competence-content-cell">
                  <div class="text-body2">{{ props.row.competence }}</div>
                </q-td>
              </q-tr>
            </template>
          </q-table>
          
          <div class="row items-center q-mb-md">
            <div class="col">
              <div class="text-caption text-grey q-mt-sm">
                <q-icon name="info" class="q-mr-xs" />
                <template v-if="filteredCompetences.length === allCompetences.length">
                  Все компетенции плана ({{ allCompetences.length }})
                </template>
                <template v-else>
                  Найдено: {{ filteredCompetences.length }} из {{ allCompetences.length }}
                </template>
              </div>
            </div>

            <div class="col-auto">
              <div class="row items-center q-gutter-sm">
                <q-btn
                  flat
                  dense
                  color="positive"
                  icon="check_box"
                  label="Выбрать все компетенции"
                  @click="selectAll"
                  :disabled="loading"
                />
                <q-btn
                  flat
                  dense
                  color="negative"
                  icon="check_box_outline_blank"
                  label="Снять все компетенции"
                  @click="unselectAll"
                  :disabled="loading"
                />
              </div>
            </div>
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

<style scoped lang="scss">
.full-height-dialog {
  width: 90vw;
  height: 90vh;
  
  .q-card__section {
    padding-bottom: 16px;
  }
}

.competence-table-container {
  height: calc(90vh - 300px); 
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

:deep(.q-table) {
  .competence-index-cell {
    text-align: center;
    vertical-align: middle;
  }
  
  .competence-content-cell {
    white-space: normal !important;
    word-break: break-word;
    line-height: 1.4;
  }
}
</style>