<template>
  <q-dialog v-model="showDialog" persistent>
    <q-card style="width: 1400px; max-width: 95vw;">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">Управление компетенциями дисциплины</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>

      <q-card-section class="q-pt-none">
        <!-- Информация о дисциплине -->
        <div class="q-mb-md">
          <div class="text-subtitle1">
            <strong>Дисциплина:</strong> {{ discipline?.index }} - {{ discipline?.name }}
          </div>
          <div class="text-caption text-blue q-mt-xs">
            <q-icon name="info" />
            Установите флаги для компетенций, которые формируются данной дисциплиной
          </div>
        </div>
        
        <!-- Статистика -->
        <div class="row q-mb-md q-gutter-md">
          <q-card flat bordered class="col-auto">
            <q-card-section class="q-pa-sm">
              <div class="text-caption text-grey">Всего компетенций</div>
              <div class="text-h6">{{ allCompetences.length }}</div>
            </q-card-section>
          </q-card>
          
          <q-card flat bordered class="col-auto">
            <q-card-section class="q-pa-sm">
              <div class="text-caption text-grey">Выбрано</div>
              <div class="text-h6 text-positive">{{ selectedCount }}</div>
            </q-card-section>
          </q-card>
          
          <q-card flat bordered class="col-auto">
            <q-card-section class="q-pa-sm">
              <div class="text-caption text-grey">Не выбрано</div>
              <div class="text-h6 text-negative">{{ unselectedCount }}</div>
            </q-card-section>
          </q-card>
        </div>
        
        <!-- Фильтры и поиск -->
        <div class="row q-mb-md q-gutter-md">
          <div class="col-12 col-md-6">
            <q-input
              v-model="searchQuery"
              placeholder="Поиск по индексу или содержанию компетенции..."
              dense
              outlined
              clearable
              class="full-width"
            >
              <template v-slot:append>
                <q-icon name="search" />
              </template>
            </q-input>
          </div>
          
          <div class="col-12 col-md-3">
            <q-select
              v-model="selectedTypeFilter"
              :options="typeOptions"
              label="Фильтр по типу"
              dense
              outlined
              clearable
              emit-value
              map-options
              class="full-width"
            />
          </div>
          
          <div class="col-12 col-md-3">
            <q-select
              v-model="selectedStatusFilter"
              :options="statusOptions"
              label="Фильтр по статусу"
              dense
              outlined
              clearable
              emit-value
              map-options
              class="full-width"
            />
          </div>
        </div>
        
        <!-- Кнопки действий -->
        <div class="row q-mb-md q-gutter-sm">
          <q-btn
            flat
            dense
            color="positive"
            icon="check_box"
            label="Выбрать все"
            @click="selectAll"
            :disabled="loading"
          />
          <q-btn
            flat
            dense
            color="negative"
            icon="check_box_outline_blank"
            label="Снять все"
            @click="unselectAll"
            :disabled="loading"
          />
          <q-btn
            flat
            dense
            color="primary"
            icon="filter_alt_off"
            label="Сбросить фильтры"
            @click="resetFilters"
            :disabled="loading"
          />
        </div>
        
        <!-- Состояние загрузки -->
        <div v-if="loading" class="text-center q-pa-lg">
          <q-spinner size="50px" color="primary" />
          <div class="q-mt-md">Загрузка данных...</div>
        </div>
        
        <!-- Таблица компетенций -->
        <div v-if="!loading">
          <q-table
            :rows="filteredCompetences"
            :columns="columns"
            row-key="competence_index"
            :loading="saving"
            :pagination="pagination"
            :rows-per-page-options="[10, 20, 50, 100]"
            binary-state-sort
            flat
            bordered
            virtual-scroll
            style="height: 500px;"
          >
            <template v-slot:top>
              <div class="text-h6">Компетенции плана ({{ filteredCompetences.length }} из {{ allCompetences.length }})</div>
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
                
                <!-- Тип компетенции -->
                <q-td key="type" :props="props">
                  <q-badge :color="getTypeColor(props.row.type)" class="q-px-sm q-py-xs">
                    {{ props.row.type }}
                  </q-badge>
                </q-td>
                
                <!-- Действия -->
                <q-td key="actions" :props="props">
                  <q-btn
                    flat
                    dense
                    round
                    icon="info"
                    color="info"
                    size="sm"
                    @click="showCompetenceDetails(props.row)"
                  >
                    <q-tooltip>Подробности</q-tooltip>
                  </q-btn>
                </q-td>
              </q-tr>
            </template>
          </q-table>
          
          <!-- Подсказка -->
          <div class="text-caption text-grey q-mt-md">
            <q-icon name="info" />
            Включите флаги для компетенций, которые формируются данной дисциплиной. 
            Все изменения сохраняются автоматически.
          </div>
        </div>
      </q-card-section>

      <q-card-actions align="right" class="q-pa-md">
        <q-btn 
          flat 
          label="Закрыть" 
          color="negative" 
          v-close-popup 
          :disabled="saving"
        />
        <q-btn 
          label="Сохранить изменения" 
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
  
  <!-- Диалог с деталями компетенции -->
  <q-dialog v-model="showDetailsDialog" persistent>
    <q-card style="width: 800px; max-width: 90vw;">
      <q-card-section class="row items-center q-pb-none">
        <div class="text-h6">Детали компетенции</div>
        <q-space />
        <q-btn icon="close" flat round dense v-close-popup />
      </q-card-section>
      
      <q-card-section v-if="selectedCompetence" class="q-pt-none">
        <div class="q-mb-md">
          <div class="text-subtitle1">
            <q-badge :color="getTypeColor(selectedCompetence.type)" class="q-mr-sm">
              {{ selectedCompetence.competence_index }}
            </q-badge>
            {{ selectedCompetence.type }}
          </div>
          <div class="text-body1 q-mt-sm">{{ selectedCompetence.competence }}</div>
        </div>
        
        <div v-if="selectedCompetence.indicators && selectedCompetence.indicators.length > 0">
          <div class="text-subtitle2 q-mb-sm">Индикаторы компетенции:</div>
          <q-list bordered separator>
            <q-item
              v-for="indicator in selectedCompetence.indicators"
              :key="indicator.index"
              class="q-py-sm"
            >
              <q-item-section>
                <q-item-label class="text-weight-medium">
                  {{ indicator.index }}
                </q-item-label>
                <q-item-label caption v-if="indicator.name">
                  {{ indicator.name }}
                </q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </div>
        
        <div v-else class="text-center q-pa-lg text-grey">
          <q-icon name="info" size="50px" />
          <div class="q-mt-md">Нет индикаторов для этой компетенции</div>
        </div>
      </q-card-section>
      
      <q-card-actions align="right">
        <q-btn flat label="Закрыть" color="primary" v-close-popup />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useCompetencePassportStore } from 'stores/competencePassportStore'
import { useQuasar } from 'quasar'
import { api } from 'boot/axios'

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
const showDialog = ref(false)
const saving = ref(false)
const loading = ref(false)
const showDetailsDialog = ref(false)
const selectedCompetence = ref(null)

// Фильтры
const searchQuery = ref('')
const selectedTypeFilter = ref(null)
const selectedStatusFilter = ref(null)

// Данные
const discipline = ref(null)
const allCompetences = ref([])
const originalCompetences = ref([])

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

// Отфильтрованные компетенции
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
    sortable: true,
    style: 'width: 100px;'
  },
  {
    name: 'competence_index',
    label: 'Индекс компетенции',
    align: 'left',
    field: row => row.competence_index,
    sortable: true,
    style: 'width: 150px;'
  },
  {
    name: 'competence',
    label: 'Содержание компетенции',
    align: 'left',
    field: row => row.competence,
    sortable: true,
    style: 'min-width: 400px;'
  },
  {
    name: 'type',
    label: 'Тип',
    align: 'center',
    field: row => row.type,
    sortable: true,
    style: 'width: 150px;'
  },
  {
    name: 'actions',
    label: 'Действия',
    align: 'center',
    style: 'width: 80px;'
  }
]

const pagination = ref({
  sortBy: 'competence_index',
  descending: false,
  page: 1,
  rowsPerPage: 20
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

function getCompetenceType(competenceIndex) {
  if (!competenceIndex) return 'Другая'
  
  if (competenceIndex.includes('УК') || competenceIndex.startsWith('УК')) return 'Универсальная'
  if (competenceIndex.includes('ОПК') || competenceIndex.startsWith('ОПК')) return 'Общепрофессиональная'
  if (competenceIndex.includes('ПК') || competenceIndex.startsWith('ПК')) return 'Профессиональная'
  if (competenceIndex.includes('ДК') || competenceIndex.startsWith('ДК')) return 'Дополнительная'
  
  return 'Другая'
}

async function loadCompetenceData() {
  loading.value = true
  try {
    const currentResponse = await api.get('/api/competence/discipline-competences-detailed/', {
      params: {
        plan_id: props.planId,
        discipline_id: props.disciplineId
      }
    })
    
    const allResponse = await api.get('/api/competence/all-competences/', {
      params: { plan_id: props.planId }
    })
    
    // Формируем объединенный список всех компетенций
    allCompetences.value = allResponse.data.competences.map(comp => {
      const isSelected = currentResponse.data.competences.some(
        c => c.competence_index === comp.competence_index && c.selected
      )
      
      const selectedComp = currentResponse.data.competences.find(
        c => c.competence_index === comp.competence_index && c.selected
      )
      
      const type = getCompetenceType(comp.competence_index)
      
      return {
        ...comp,
        selected: isSelected,
        type: type,
        type_short: getShortType(type),
        indicators_count: selectedComp ? selectedComp.indicators_count : 0,
        indicators: selectedComp ? selectedComp.indicators : []
      }
    })
    
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
    // При выборе компетенции создаем пустые индикаторы
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

function showCompetenceDetails(competence) {
  selectedCompetence.value = competence
  showDetailsDialog.value = true
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
  
  const confirmed = await $q.dialog({
    title: 'Подтверждение сохранения',
    message: `Вы уверены, что хотите сохранить изменения для ${selectedCount.value} компетенций?`,
    html: true,
    cancel: true,
    persistent: true,
    ok: {
      label: 'Сохранить',
      color: 'positive'
    }
  })
  
  if (!confirmed) return
  
  saving.value = true
  try {
    const selectedCompetences = allCompetences.value
      .filter(comp => comp.selected)
      .map(comp => ({
        competence_index: comp.competence_index,
        competence: comp.competence,
        indicators: comp.indicators || []
      }))
    
    const response = await api.post('/api/competence/update-discipline-competences/', {
      plan_id: props.planId,
      discipline_id: props.disciplineId,
      selected_competences: selectedCompetences
    })
    
    $q.notify({
      type: 'positive',
      message: `Успешно сохранено ${selectedCompetences.length} компетенций`,
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
    // Сбрасываем фильтры и загружаем данные
    resetFilters()
    loadCompetenceData()
  } else {
    // Сбрасываем состояние при закрытии
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
.competence-table {
  .q-table {
    .q-badge {
      font-size: 12px;
      font-weight: 500;
    }
    
    .q-toggle {
      transform: scale(0.9);
    }
    
    .q-chip {
      height: 20px;
      font-size: 11px;
    }
  }
}

.text-ellipsis {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>