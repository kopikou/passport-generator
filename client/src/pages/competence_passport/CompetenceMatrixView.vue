<script setup lang="ts">
import { ref, computed, onBeforeMount, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useQuasar, date } from 'quasar'
import { useCompetencePassportStore } from 'src/stores/competencePassportStore'
import { storeToRefs } from 'pinia'
import MatrixEditor from './components/MatrixEditor.vue'

const route = useRoute()
const $q = useQuasar()
const store = useCompetencePassportStore()

const {
  currentPlanId,
  matrix,
  disciplines,
  loading,
  validating,
  matrixValidation,
} = storeToRefs(store)

const searchFilter = ref('')
const expandedGroups = ref(new Set<string>())
const showEditor = ref(false)
const editingRow = ref<any>(null)
const showValidationDetails = ref(false)
const highlightedDiscipline = ref<string | null>(null)
const exporting = ref(false)

async function exportMatrix() {
  exporting.value = true
  try {
    store.getMatrixReport()    
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: 'Ошибка при генерации документа',
      position: 'top-right'
    })
  } finally {
    exporting.value = false
  }
}

const columns = [
  {
    name: 'discipline_index',
    label: 'Индекс',
    align: 'left',
    field: (row: any) => row.discipline_index,
    sortable: true,
    style: 'width: 180px; min-width: 180px; max-width: 180px;'
  },
  {
    name: 'discipline_name',
    label: 'Наименование',
    align: 'left',
    field: (row: any) => row.discipline_name,
    sortable: true,
    style: 'width: 400px; min-width: 400px; max-width: 400px;'
  },
  {
    name: 'competence_indices',
    label: 'Формируемые компетенции',
    align: 'left',
    field: (row: any) => {
      if (!row.competence_list || !Array.isArray(row.competence_list)) return ''
      return row.competence_list.map((c: any) => c.competence_index).join(', ')
    },
    sortable: false,
    style: 'width: calc(100vw - 650px); min-width: 400px; max-width: calc(100vw - 650px);'
  }
]

// Вычисляемые свойства
const validationStatus = computed(() => {
  if (validating.value) {
    return {
      type: 'info',
      title: 'Проверка матрицы...',
      message: 'Идет проверка связей между дисциплинами и компетенциями',
      details: false
    }
  }

  if (matrixValidation.value?.is_valid) {
    return {
      type: 'success',
      title: 'Матрица компетенций проверена успешно!',
      message: 'Все требования выполнены.',
      details: true
    }
  }

  if (matrixValidation.value?.errors?.length > 0) {
    const discErrors = matrixValidation.value.errors.filter(e => e.discipline_id)
    const compErrors = matrixValidation.value.errors.filter(e => e.competence_index && 
    !e.message.includes('преддиплом') && !e.message.includes('общепроф') && 
    !e.message.includes('только практиками'))
    const practiceErrors = matrixValidation.value.errors.filter(e => e.message.includes('преддиплом'))
    const opkPracticeError = matrixValidation.value.errors.filter(e => e.message.includes('общепроф')) 
    const onlyPracticeErrors = matrixValidation.value.errors.filter(e => e.message.includes('только практиками'))
    
    let message = ''
    if (discErrors.length > 0) message += `${discErrors.length} дисциплин без компетенций, `
    if (compErrors.length > 0) message += `${compErrors.length} компетенций без дисциплин, `
    if (practiceErrors.length > 0) message += `${practiceErrors.length} проф. компетенций без преддипломной практики,`
    if (opkPracticeError.length > 0) message += `отсутствует ОПК в практиках,`
    if (onlyPracticeErrors.length > 0) message += `${onlyPracticeErrors.length} компетенций только в практиках`
    
    message = message.replace(/, $/, '') 
    
    return {
      type: 'error',
      title: 'Найдены проблемы в матрице компетенций',
      message: `Необходимо исправить: ${message}`,
      details: true
    }
  }

  return null
})

const lastCheckedFormatted = computed(() => {
  if (!matrixValidation.value?.checked_at) return 'еще не проверялась'
  return date.formatDate(matrixValidation.value.checked_at, 'DD.MM.YYYY HH:mm:ss')
})

// Методы иерархии дисциплин
function hasChildren(groupIndex) {
  return matrix.value.some(item =>  
    item.discipline_index !== groupIndex && 
    item.discipline_index.startsWith(groupIndex + '.')
  )
}

function isExpanded(groupIndex) {
  return expandedGroups.value.has(groupIndex)
}

function toggleGroup(groupIndex) {
  if (expandedGroups.value.has(groupIndex)) {
    expandedGroups.value.delete(groupIndex)
  } else {
    expandedGroups.value.add(groupIndex)
  }
}

function expandAll() {
  matrix.value.forEach(item => {
    if (item.type === 'group' && hasChildren(item.discipline_index)) {
      expandedGroups.value.add(item.discipline_index)
    }
  })
}

function collapseAll() {
  expandedGroups.value.clear()
}

function getParentGroups(itemIndex) {
  const parents = []
  const parts = itemIndex.split('.')
  for (let i = 1; i < parts.length; i++) {
    const parentIndex = parts.slice(0, i).join('.')
    parents.push(parentIndex)
  }
  return parents
}

function isItemVisible(item) {
  const parentGroups = getParentGroups(item.discipline_index)
  for (const parentIndex of parentGroups) {
    const parentItem = matrix.value.find(g => g.discipline_index === parentIndex && g.type === 'group')
    if (parentItem && !expandedGroups.value.has(parentIndex)) {
      return false
    }
  }
  return true
}

// Фильтрация
const filteredMatrix = computed(() => {
  const term = (searchFilter.value || '').trim().toLowerCase()
  
  if (!term) {
    return matrix.value
  }
  const visibleItems = new Set<string>()
  
  matrix.value.forEach(item => {
    const matches = 
      item.discipline_index.toLowerCase().includes(term) ||
      item.discipline_name.toLowerCase().includes(term) ||
      (item.competence_list && Array.isArray(item.competence_list) && 
       item.competence_list.some((comp: any) =>
         comp.competence_index.toLowerCase().includes(term) ||
         comp.competence.toLowerCase().includes(term)
       ))
    
    if (matches) {
      visibleItems.add(item.discipline_index)
      let current = item.discipline_index
      while (current.includes('.')) {
        current = current.substring(0, current.lastIndexOf('.'))
        visibleItems.add(current)
      }
    }
  })
  
  return matrix.value.filter(item => visibleItems.has(item.discipline_index))
})


const visibleMatrix = computed(() => {
  return filteredMatrix.value.filter(item => isItemVisible(item))
})

function getCompetenceBadgeColor(type) {
  const colors: Record<string, string> = {
    'Универсальная': 'blue',
    'Общепрофессиональная': 'green',
    'Профессиональная': 'orange',
    'Дополнительная': 'purple'
  }
  return colors[type] || 'grey'
}

function isDisciplineWithoutCompetences(disciplineIndex) {
  return matrixValidation.value?.errors?.some(
    error => error.discipline_index === disciplineIndex
  ) || false
}

function scrollToDiscipline(disciplineIndex) {
  highlightedDiscipline.value = disciplineIndex
  showValidationDetails.value = false
  
  setTimeout(() => {
    const row = document.querySelector(`tr[data-index="${CSS.escape(disciplineIndex)}"]`)
    if (row) {
      row.scrollIntoView({ behavior: 'smooth', block: 'center' })
      row.classList.add('blink-animation')
      setTimeout(() => row.classList.remove('blink-animation'), 2000)
    }
  }, 100)
}

// Загрузка и валидация
async function loadMatrixData() {
  await store.fetchMatrix(currentPlanId.value)
  //await store.validateMatrix()

  matrix.value.forEach(item => {
    if (item.type === 'group' && item.level === 1 && hasChildren(item.discipline_index)) {
      expandedGroups.value.add(item.discipline_index)
    }
  })
}

async function runMatrixValidation() {
  await store.validateMatrix()
  //   await store.validateMatrix()
    
  //   if (matrixValidation.value?.is_valid) {
  //     $q.notify({
  //       type: 'positive',
  //       message: 'Матрица компетенций проверена успешно!',
  //       position: 'top-right',
  //       timeout: 3000
  //     })
  //   } else {
  //     $q.notify({
  //       type: 'warning',
  //       message: 'Найдены проблемы в матрице компетенций',
  //       position: 'top-right',
  //       timeout: 5000,
  //       actions: [{ label: 'Показать детали', color: 'white', handler: () => {
  //         showValidationDetails.value = true
  //       }}]
  //     })
  //   }
}

// Редактирование
async function onRowClick(row) {
  if (row.type !== 'discipline') return
  
  const discipline = disciplines.value.find(d => d.discipline_id === row.discipline_id)
  if (!discipline) return
  
  editingRow.value = {
    id: discipline.discipline_id,
    index: discipline.discipline_index,
    name: discipline.discipline_name
  }
  showEditor.value = true
}

function onCompetencesSaved() {
  showEditor.value = false
  editingRow.value = null
  $q.notify({ 
    type: 'positive', 
    message: 'Компетенции успешно обновлены',
    position: 'top-right'
  })
  loadMatrixData()
}

onBeforeMount(() => {
  loadMatrixData()
  runMatrixValidation()
})

watch(() => route.params.id, () => {
  loadMatrixData()
})
</script>

<template>
  <div class="q-pa-md q-mb-lg">
    <!-- Блок валидации -->
    <div v-if="validationStatus" class="q-mb-md validation-container">
      <q-banner 
        :class="validationStatus.type === 'error' ? 'bg-negative text-white' : 'bg-positive text-white'"
        rounded
      >
        <template v-slot:avatar>
          <q-icon :name="validationStatus.type === 'error' ? 'warning' : 'check_circle'" size="24px" />
        </template>
        
        <div class="text-body1 q-mb-xs">{{ validationStatus.title }}</div>
        <div class="text-body2">{{ validationStatus.message }}</div>
        
        <template v-if="validationStatus.details" v-slot:action>
          <q-btn 
            flat 
            :color="validationStatus.type === 'error' ? 'white' : 'dark'" 
            :label="showValidationDetails ? 'Скрыть детали' : 'Показать детали'" 
            @click="showValidationDetails = !showValidationDetails"
            class="q-mr-sm"
          />
          <q-btn 
            v-if="validationStatus.type === 'error'"
            flat 
            :color="validationStatus.type === 'error' ? 'white' : 'dark'" 
            label="Обновить проверку" 
            @click="runMatrixValidation"
            :loading="validating"
            icon="refresh"
          />
        </template>
      </q-banner>
      
      <q-slide-transition>
        <div v-if="showValidationDetails && validationStatus.details" class="validation-details q-pa-md bg-grey-2 q-mt-sm">
          <div v-if="matrixValidation?.errors?.filter(e => e.discipline_id).length" class="q-mb-md">
            <div class="text-subtitle1 text-weight-medium q-mb-sm">
              <q-icon name="error_outline" color="negative" class="q-mr-xs" />
              Дисциплины без компетенций:
            </div>
            <div class="q-gutter-sm">
              <q-chip 
                v-for="error in matrixValidation.errors.filter(e => e.discipline_id)"
                :key="error.discipline_index"
                color="negative" 
                text-color="white"
                icon="school"
                clickable
                @click="scrollToDiscipline(error.discipline_index)"
              >
                {{ error.discipline_index }} - {{ error.discipline_name }}
              </q-chip>
            </div>
          </div>
          
          <div v-if="matrixValidation?.errors?.filter(e => e.competence_index && !e.message.includes('преддиплом') && !e.message.includes('общепроф') && !e.message.includes('только практиками')).length" class="q-mb-md">
            <div class="text-subtitle1 text-weight-medium q-mb-sm">
              <q-icon name="error_outline" color="negative" class="q-mr-xs" />
              Компетенции без дисциплин:
            </div>
            <div class="q-gutter-sm">
              <q-chip 
                v-for="error in matrixValidation.errors.filter(e => e.competence_index)"
                :key="error.competence_index"
                color="negative" 
                text-color="white"
                icon="school"
              >
                {{ error.competence_index }}
                <q-tooltip>{{ error.competence }}</q-tooltip>
              </q-chip>
            </div>
          </div>

          <div v-if="matrixValidation?.errors?.filter(e => e.message.includes('преддиплом')).length" class="q-mb-md">
            <div class="text-subtitle1 text-weight-medium q-mb-sm">
              <q-icon name="error_outline" color="negative" class="q-mr-xs" />
              Профессиональные компетенции без преддипломной практики:
            </div>
            <div class="q-gutter-sm">
              <q-chip 
                v-for="error in matrixValidation.errors.filter(e => e.message.includes('преддиплом'))"
                :key="error.competence_index"
                color="negative" 
                text-color="white"
                icon="school"
              >
                {{ error.competence_index }}
                <q-tooltip>{{ error.competence }}</q-tooltip>
              </q-chip>
            </div>
          </div>

          <div v-if="matrixValidation?.errors?.filter(e => e.message.includes('общепроф')).length" class="q-mb-md">
            <div class="text-subtitle1 text-weight-medium q-mb-sm">
              <q-icon name="error_outline" color="negative" class="q-mr-xs" />
              Отсутствует формирование ОПК в практиках:
            </div>
            <div class="q-gutter-sm">
              <q-chip 
                color="negative" 
                text-color="white"
                icon="school"
              >
                Хотя бы одна практика должна формировать общепрофессиональную компетенцию
              </q-chip>
            </div>
          </div>

          <div v-if="matrixValidation?.errors?.filter(e => e.message.includes('только практиками')).length" class="q-mb-md">
          <div class="text-subtitle1 text-weight-medium q-mb-sm">
            <q-icon name="error_outline" color="negative" class="q-mr-xs" />
            Компетенции только в практиках:
          </div>
          <div class="q-gutter-sm">
            <q-chip 
              v-for="error in matrixValidation.errors.filter(e => e.message.includes('только практиками'))"
              :key="error.competence_index"
              color="negative" 
              text-color="white"
              icon="school"
            >
              {{ error.competence_index }}
              <q-tooltip>{{ error.competence }}</q-tooltip>
            </q-chip>
          </div>
        </div>
          
          <div class="text-caption">
            <q-icon name="info" class="q-mr-xs" />
            Проверка выполнена: {{ lastCheckedFormatted }}
          </div>
        </div>
      </q-slide-transition>
    </div>

    <!-- Шапка -->
    <div class="row items-center q-mb-md">
      <div class="col">
        <h2 class="text-h4 q-ma-none">Матрица компетенций</h2>
        <div class="text-subtitle1 text-grey">
          Соответствие дисциплины и формируемых компетенций
        </div>
        <div class="text-subtitle1 text-grey">
          Окно редактора вызывается щелчком мыши в необходимой строке
        </div>
      </div>
      
      <div class="col-auto">
        <div class="row items-center q-gutter-sm  q-mb-md">
          <q-btn flat dense color="primary" icon="expand_more" @click="expandAll" label="Раскрыть все" class="q-mr-sm" />
          <q-btn flat dense color="primary" icon="expand_less" @click="collapseAll" label="Свернуть все" class="q-mr-sm" />
          <q-btn
            flat
            dense
            color="primary"
            icon="check_circle"
            label="Проверить"
            @click="runMatrixValidation"
            :loading="validating"
            class="q-mr-sm"
          >
            <q-tooltip>Проверить связи между дисциплинами и компетенциями</q-tooltip>
          </q-btn>
          <q-input
            v-model="searchFilter"
            placeholder="Поиск по дисциплинам, группам или индексам..."
            dense
            outlined
            clearable
            style="min-width: 200px;"
          >
            <template v-slot:append>
              <q-icon name="search" />
            </template>
          </q-input>

          <q-btn
            flat
            dense
            icon="file_download"
            label="Выгрузить"
            @click="exportMatrix"
            :loading="exporting"
            class="q-mr-sm q-pr-sm bg-primary text-white"
          >
            <q-tooltip>Скачать матрицу компетенций в формате Word</q-tooltip>
          </q-btn>
        </div>
      </div>
    </div>

    <!-- Таблица -->
    <q-table
      :rows="visibleMatrix"
      :columns="columns"
      row-key="discipline_index"
      :loading="loading"
      :pagination="{ sortBy: 'discipline_index', descending: false, page: 1, rowsPerPage: 0 }"
      binary-state-sort
      flat
      bordered
      style="height: auto;"
    >
      <template v-slot:top>
        <div class="text-h6">
          Показано строк: {{ visibleMatrix.length }} из {{ matrix.length }}
        </div>
        <q-space />
        <div class="text-caption text-grey" v-if="searchFilter">
          Поиск: "{{ searchFilter }}"
        </div>
      </template>

      <template v-slot:body="props">
        <q-tr 
          :props="props" 
          :class="[
            { 'clickable-row': props.row.type === 'discipline' },
            { 'row-without-competences': props.row.type === 'discipline' && isDisciplineWithoutCompetences(props.row.discipline_index) },
            { 'highlighted-row': props.row.discipline_index === highlightedDiscipline }
          ]"
          @click="onRowClick(props.row)"
          :data-index="props.row.discipline_index"
        >
          <q-td key="discipline_index" :props="props">
            <div 
              :class="[
                'text-weight-medium',
                props.row.type === 'group' ? 'text-primary' : 'text-grey-8',
                `level-${props.row.level}`
              ]"
              :style="{ marginLeft: `${(props.row.level - 1) * 20}px`, display: 'flex', alignItems: 'center' }"
            >
              <q-btn
                v-if="props.row.type === 'group' && hasChildren(props.row.discipline_index)"
                flat
                dense
                round
                size="sm"
                icon="keyboard_arrow_down"
                :class="{ 'rotate-180': isExpanded(props.row.discipline_index) }"
                @click.stop="toggleGroup(props.row.discipline_index)"
                class="q-mr-xs transition-transform"
                style="min-width: 24px; min-height: 24px;"
              />
              <span style="width: 16px; display: inline-block;" v-else></span>
              
              <q-icon 
                v-if="props.row.type === 'discipline' && isDisciplineWithoutCompetences(props.row.discipline_index)"
                name="error_outline" 
                color="negative" 
                size="16px"
                class="q-mr-xs"
              >
                <q-tooltip>У этой дисциплины нет компетенций</q-tooltip>
              </q-icon>
              
              {{ props.row.discipline_index }}
            </div>
          </q-td>
          
          <q-td key="discipline_name" :props="props">
            <div 
              :class="[
                props.row.type === 'group' ? 'text-bold' : '',
                `level-${props.row.level} ${props.row.type}-type`,
                { 'text-negative': props.row.type === 'discipline' && isDisciplineWithoutCompetences(props.row.discipline_index) }
              ]"
            >
              {{ props.row.discipline_name }}
            </div>
          </q-td>
          
          <q-td key="competence_indices" :props="props">
            <div v-if="props.row.competence_list && props.row.competence_list.length" >
              <q-badge
                v-for="comp in props.row.competence_list"
                :key="comp.competence_index"
                :color="getCompetenceBadgeColor(comp.type)"
                class="q-mx-xs q-my-xs q-px-sm q-py-xs"
                style="display: inline-block;"
              >
                {{ comp.competence_index }}
              </q-badge>
            </div>
            <div v-else class="text-grey text-italic">
              <q-icon name="warning" color="negative" class="q-mr-xs" />
              Нет компетенций
            </div>
          </q-td>
        </q-tr>
      </template>
    </q-table>
    
    <!-- Редактор -->
    <MatrixEditor
      v-if="editingRow"
      :plan-id="currentPlanId"
      :discipline-id="editingRow.id"
      :discipline-index="editingRow.index"
      :discipline-name="editingRow.name"
      :show="showEditor"
      @update:show="showEditor = $event"
      @saved="onCompetencesSaved"
    />
  </div>
</template>

<style scoped lang="scss">
.validation-container {
  .q-banner {
    border-left: 4px solid;
    
    &.bg-negative {
      border-left-color: darken(#f44336, 10%);
    }
    
    &.bg-positive {
      border-left-color: darken(#4CAF50, 10%);
    }
  }
}

.validation-details {
  border-radius: 0 0 8px 8px;
  border: 1px solid rgba(0,0,0,0.1);
  border-top: none;
}

.validation-status-indicator {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.row-without-competences {
  background-color: rgba(244, 67, 54, 0.08) !important;
  border-left: 4px solid #f44336 !important;
  
  &:hover {
    background-color: rgba(244, 67, 54, 0.12) !important;
  }
}

.highlighted-row {
  background-color: rgba(255, 193, 7, 0.15) !important;
  border: 2px solid #ffc107 !important;
  position: relative;

}

.blink-animation {
  animation: blink 1s 3;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.level-1 {
  font-size: 16px;
  font-weight: bold;
}

.level-2 {
  font-size: 15px;
  font-weight: 600;
}

.level-3 {
  font-size: 14px;
}

.level-4 {
  font-size: 13px;
}

.level-5 {
  font-size: 12px;
}

.clickable-row {
  cursor: pointer;
  
  &:hover {
    background-color: rgba(0, 0, 0, 0.04);
  }
  
  &:active {
    background-color: rgba(0, 0, 0, 0.08);
  }
}

.transition-transform {
  transition: transform 0.3s ease;
}

:deep(.q-table) {
  .q-badge {
    font-size: 12px;
    line-height: 1.2;
    margin: 2px 4px 2px 0; 
    white-space: nowrap;
  }
}

:deep(table) {
  table-layout: fixed;
  width: 100%;
  
  th, td {
    text-overflow: ellipsis;
    white-space: normal;
  }
}

</style>