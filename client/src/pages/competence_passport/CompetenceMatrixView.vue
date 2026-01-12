<template>
  <top-navigation-menu>
    <template #content>
      <div class="q-pa-md q-mb-lg">
        <!-- Блок с валидацией матрицы -->
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
                :loading="matrixValidation.validationInProgress"
                icon="refresh"
              />
            </template>
          </q-banner>
          
          <!-- Детали валидации -->
          <q-slide-transition>
            <div v-if="showValidationDetails && validationStatus.details" class="validation-details q-pa-md bg-grey-2 q-mt-sm">
              <!-- Дисциплины без компетенций -->
              <div v-if="matrixValidation.disciplinesWithoutCompetences.length > 0" class="q-mb-md">
                <div class="text-subtitle1 text-weight-medium q-mb-sm">
                  <q-icon name="error_outline" color="negative" class="q-mr-xs" />
                  Дисциплины без компетенций ({{ matrixValidation.disciplinesWithoutCompetences.length }}):
                </div>
                <div class="q-gutter-sm">
                  <q-chip 
                    v-for="disc in matrixValidation.disciplinesWithoutCompetences" 
                    :key="disc.index"
                    color="negative" 
                    text-color="white"
                    icon="school"
                    clickable
                    @click="scrollToDiscipline(disc.index)"
                    class="cursor-pointer"
                  >
                    {{ disc.index }} - {{ disc.name }}
                  </q-chip>
                </div>
                <div class="text-caption text-grey q-mt-xs">
                  Нажмите на дисциплину для быстрого перехода к ней в таблице
                </div>
              </div>
              
              <!-- Компетенции без дисциплин -->
              <div v-if="matrixValidation.competencesWithoutDisciplines.length > 0" class="q-mb-md">
                <div class="text-subtitle1 text-weight-medium q-mb-sm">
                  <q-icon name="warning" color="warning" class="q-mr-xs" />
                  Компетенции без дисциплин ({{ matrixValidation.competencesWithoutDisciplines.length }}):
                </div>
                <div class="q-gutter-sm">
                  <q-chip 
                    v-for="comp in matrixValidation.competencesWithoutDisciplines" 
                    :key="comp.competence_index"
                    color="warning" 
                    text-color="dark"
                    icon="assignment"
                  >
                    {{ comp.competence_index }}
                    <q-tooltip>
                      {{ comp.competence }}
                    </q-tooltip>
                  </q-chip>
                </div>
                <div class="text-caption text-grey q-mt-xs">
                  Эти компетенции не привязаны ни к одной дисциплине плана
                </div>
              </div>
              
              <!-- Сводка -->
              <div class="row items-center justify-between q-mt-md">
                <div class="col">
                  <div class="text-caption">
                    <q-icon name="info" class="q-mr-xs" />
                    Проверка выполнена: {{ lastCheckedFormatted }}
                  </div>
                </div>
              </div>
            </div>
          </q-slide-transition>
        </div>

        <div class="row items-center q-mb-md">
          <div class="col">
            <h2 class="text-h4 q-ma-none">Матрица компетенций</h2>
            <div class="text-subtitle1 text-grey">
              Соответствие дисциплины и формируемых компетенций
            </div>
            <div class="text-subtitle1 text-grey">
              Окно редактора вызывается щелчком мыши в необходимой строке
            </div>
            
            <!-- Статус валидации в шапке -->
            <div v-if="validationStatus" class="validation-status-indicator q-mt-sm">   
              <span class="q-ml-sm text-caption">
                <span v-if="matrixValidation.disciplinesWithoutCompetences.length > 0">
                  {{ matrixValidation.disciplinesWithoutCompetences.length }} дисциплин без компетенций
                </span>
                <span v-if="matrixValidation.disciplinesWithoutCompetences.length > 0 && matrixValidation.competencesWithoutDisciplines.length > 0">
                  , 
                </span>
                <span v-if="matrixValidation.competencesWithoutDisciplines.length > 0">
                  {{ matrixValidation.competencesWithoutDisciplines.length }} компетенций без дисциплин
                </span>
              </span>
            </div>
          </div>
          
          <div class="col-auto">
            <!-- Кнопки управления матрицей -->
            <div class="row items-center q-gutter-sm">
              <q-btn
                flat
                dense
                color="primary"
                icon="expand_more"
                @click="expandAll"
                label="Раскрыть все"
                class="q-mr-sm"
              />
              <q-btn
                flat
                dense
                color="primary"
                icon="expand_less"
                @click="collapseAll"
                label="Свернуть все"
                class="q-mr-sm"
              />
              
              <!-- Кнопка проверки матрицы -->
              <q-btn
                flat
                dense
                color="primary"
                icon="check_circle"
                label="Проверить"
                @click="runMatrixValidation"
                :loading="matrixValidation.validationInProgress"
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
                style="min-width: 300px;"
              >
                <template v-slot:append>
                  <q-icon name="search" />
                </template>
              </q-input>
            </div>
          </div>
        </div>

        <!-- Таблица матрицы -->
        <q-table
          :rows="visibleMatrix"
          :columns="columns"
          row-key="index"
          :loading="matrixLoading"
          :pagination="pagination"
          binary-state-sort
          flat
          bordered
          style="height: auto;"
          :class="{ 'has-validation-errors': validationStatus?.type === 'error' }"
        >
          <template v-slot:top>
            <div class="text-h6">
              Показано строк: {{ visibleMatrix.length }} из {{ competenceMatrix.length }}
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
                { 'row-without-competences': props.row.type === 'discipline' && isDisciplineWithoutCompetences(props.row.index) },
                { 'highlighted-row': props.row.index === highlightedDiscipline }
              ]"
              @click="onRowClick(props.row)"
              :data-index="props.row.index"
            >
              <q-td key="index" :props="props">
                <div 
                  :class="[
                    'text-weight-medium',
                    props.row.type === 'group' ? 'text-primary' : 'text-grey-8',
                    `level-${props.row.level}`
                  ]"
                  :style="{ marginLeft: `${(props.row.level - 1) * 20}px`, display: 'flex', alignItems: 'center' }"
                >
                  <q-btn
                    v-if="props.row.type === 'group' && hasChildren(props.row.index)"
                    flat
                    dense
                    round
                    size="sm"
                    icon="keyboard_arrow_down"
                    :class="{ 'rotate-180': isExpanded(props.row.index) }"
                    @click.stop="toggleGroup(props.row.index)"
                    class="q-mr-xs transition-transform"
                    style="min-width: 24px; min-height: 24px;"
                  />
                  <q-icon 
                    v-else-if="props.row.type === 'group'" 
                    :name="getGroupIcon(props.row.level)" 
                    class="q-mr-xs"
                    size="16px"
                  />
                  <span style="width: 16px; display: inline-block;" v-else></span>
                  
                  <!-- Индикатор проблемной дисциплины -->
                  <q-icon 
                    v-if="props.row.type === 'discipline' && isDisciplineWithoutCompetences(props.row.index)"
                    name="error_outline" 
                    color="negative" 
                    size="16px"
                    class="q-mr-xs"
                  >
                    <q-tooltip>У этой дисциплины нет компетенций</q-tooltip>
                  </q-icon>
                  
                  {{ props.row.index }}
                </div>
              </q-td>
              
              <q-td key="name" :props="props">
                <div 
                  :class="[
                    props.row.type === 'group' ? 'text-bold' : '',
                    `level-${props.row.level} ${props.row.type}-type`,
                    { 'text-negative': props.row.type === 'discipline' && isDisciplineWithoutCompetences(props.row.index) }
                  ]"
                >
                  {{ props.row.name }}
                </div>
              </q-td>
              
              <q-td key="competence_indices" :props="props">
                <div v-if="props.row.competence_indices" class="competence-indices-cell">
                  <template v-for="(index, idx) in props.row.competence_indices.split(', ')" :key="idx">
                    <q-badge 
                      :color="getCompetenceBadgeColor(index)"
                      class="q-mx-xs q-my-xs q-px-sm q-py-xs"
                      style="display: inline-block;"
                    >
                      {{ index }}
                    </q-badge>
                    <br v-if="(idx + 1) % 5 === 0" />
                  </template>
                </div>
                <div v-else class="text-grey text-italic">
                  <q-icon name="warning" color="negative" class="q-mr-xs" />
                  Нет компетенций
                </div>
              </q-td>
            </q-tr>
          </template>
          
          <template v-slot:no-data>
            <div class="full-width row flex-center q-gutter-sm">
              <q-icon name="info" size="2em" />
              <span>Нет данных для отображения</span>
            </div>
          </template>
        </q-table>
        
        <!-- Модальное окно редактирования -->
        <discipline-competences-editor
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
  </top-navigation-menu>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, onUnmounted, nextTick } from 'vue'
import { useCompetencePassportStore } from 'stores/competencePassportStore'
import { useRouter } from 'vue-router'
import TopNavigationMenu from './components/TopNavigationMenu.vue'
import DisciplineCompetencesEditor from './components/DisciplineCompetencesEditor.vue'
import { storeToRefs } from 'pinia'
import { useQuasar, date } from 'quasar'

const $q = useQuasar()
const router = useRouter()
const store = useCompetencePassportStore()
const {
  competenceMatrix,
  matrixLoading,
  currentPlanId,
  matrixValidation,
  currentPlanDisciplines,
  saving
} = storeToRefs(store)

const searchFilter = ref('')
const currentPlan = ref(null)
const expandedGroups = ref(new Set())
const pagination = ref({
  sortBy: 'index',
  descending: false,
  page: 1,
  rowsPerPage: 0
})

const showEditor = ref(false)
const editingRow = ref(null)
const disciplinesMap = ref({})

const showValidationDetails = ref(false)
const highlightedDiscipline = ref(null)

const columns = [
  {
    name: 'index',
    required: true,
    label: 'Индекс',
    align: 'left',
    field: row => row.index,
    sortable: true,
    style: 'width: 180px; min-width: 180px; max-width: 180px;'
  },
  {
    name: 'name',
    required: true,
    label: 'Наименование',
    align: 'left',
    field: row => row.name,
    sortable: true,
    style: 'width: 400px; min-width: 400px; max-width: 400px;'
  },
  {
    name: 'competence_indices',
    label: 'Формируемые компетенции',
    align: 'left',
    field: row => row.competence_indices,
    sortable: false,
    style: 'width: calc(100vw - 650px); min-width: 400px; max-width: calc(100vw - 650px);'
  }
]

const validationStatus = computed(() => {
  const validation = matrixValidation.value
  
  if (validation.validationInProgress) {
    return {
      type: 'info',
      title: 'Проверка матрицы...',
      message: 'Идет проверка связей между дисциплинами и компетенциями',
      details: false
    }
  }
  
  if (validation.isValid) {
    return {
      type: 'success',
      title: 'Матрица компетенций проверена успешно!',
      message: 'Все дисциплины имеют компетенции и все компетенции привязаны к дисциплинам.',
      details: true
    }
  } else if (validation.disciplinesWithoutCompetences.length > 0 || 
             validation.competencesWithoutDisciplines.length > 0) {
    return {
      type: 'error',
      title: 'Найдены проблемы в матрице компетенций',
      message: `Необходимо исправить ${validation.disciplinesWithoutCompetences.length} дисциплин без компетенций и ${validation.competencesWithoutDisciplines.length} компетенций без дисциплин`,
      details: true
    }
  }
  
  return null
})

const lastCheckedFormatted = computed(() => {
  if (!matrixValidation.value.lastChecked) return 'еще не проверялась'
  
  const timeStamp = date.formatDate(
    matrixValidation.value.lastChecked, 
    'DD.MM.YYYY HH:mm:ss'
  )
  
  return timeStamp
})

const filteredMatrix = computed(() => {
  let filtered = competenceMatrix.value
  
  if (searchFilter.value) {
    const searchLower = searchFilter.value.toLowerCase()
    filtered = filtered.filter(item => 
      item.index.toLowerCase().includes(searchLower) ||
      item.name.toLowerCase().includes(searchLower) ||
      (item.competence_indices && item.competence_indices.toLowerCase().includes(searchLower))
    )
  }
  
  return filtered
})

const visibleMatrix = computed(() => {
  return filteredMatrix.value.filter(item => isItemVisible(item))
})

function getCompetenceBadgeColor(competenceIndex) {
  if (!competenceIndex) return 'grey'
  
  if (competenceIndex.includes('УК') || competenceIndex.startsWith('УК')) return 'blue'
  if (competenceIndex.includes('ОПК') || competenceIndex.startsWith('ОПК')) return 'green'
  if (competenceIndex.includes('ПК') || competenceIndex.startsWith('ПК')) return 'orange'
  if (competenceIndex.includes('ДК') || competenceIndex.startsWith('ДК')) return 'purple'
  
  return 'grey'
}

function getGroupIcon(level) {
  const icons = [
    'folder',
    'folder_open',
    'folder',
    'folder_open',
    'folder'
  ]
  return icons[level - 1] || 'folder'
}

function hasChildren(groupIndex) {
  const allItems = competenceMatrix.value
  return allItems.some(item => 
    item.index !== groupIndex && 
    item.index.startsWith(groupIndex + '.')
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
  const allItems = competenceMatrix.value
  allItems.forEach(item => {
    if (item.type === 'group' && hasChildren(item.index)) {
      expandedGroups.value.add(item.index)
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
  const parentGroups = getParentGroups(item.index)
  
  for (const parentIndex of parentGroups) {
    const parentItem = competenceMatrix.value.find(g => g.index === parentIndex && g.type === 'group')
    if (parentItem && !expandedGroups.value.has(parentIndex)) {
      return false
    }
  }
  
  return true
}

// Валидационные методы
function isDisciplineWithoutCompetences(disciplineIndex) {
  return matrixValidation.value.disciplinesWithoutCompetences.some(
    disc => disc.index === disciplineIndex
  )
}

function scrollToDiscipline(disciplineIndex) {
  highlightedDiscipline.value = disciplineIndex
  showValidationDetails.value = false
  
  // Прокрутка к дисциплине
  setTimeout(() => {
  const row = document.querySelector(`tr[data-index="${CSS.escape(disciplineIndex)}"]`)
    if (row) {
      row.scrollIntoView({ behavior: 'smooth', block: 'center' })
      row.classList.add('blink-animation')
      setTimeout(() => row.classList.remove('blink-animation'), 2000)
    }
  }, 100)
}
async function runMatrixValidation() {
  try {
    const result = await store.validateCompetenceMatrix(currentPlanId.value)
    
    if (result.isValid) {
      $q.notify({
        type: 'positive',
        message: 'Матрица компетенций проверена успешно! Все связи установлены.',
        position: 'top-right',
        timeout: 3000
      })
      localStorage.setItem(`matrix_valid_${currentPlanId.value}`, 'true')
    } else {
      $q.notify({
        type: 'warning',
        message: `Найдены проблемы: ${result.disciplinesWithoutCompetences.length} дисциплин без компетенций, ${result.competencesWithoutDisciplines.length} компетенций без дисциплин`,
        position: 'top-right',
        timeout: 5000,
        actions: [
          { label: 'Показать детали', color: 'white', handler: () => {
            showValidationDetails.value = true
          }}
        ]
      })
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: `Ошибка при проверке матрицы: ${error.message}`,
      position: 'top-right'
    })
  }
}

async function loadDisciplines() {
  if (!currentPlanId.value) return
  
  try {
    await store.fetchAllDisciplines(currentPlanId.value)
    
    disciplinesMap.value = {}
    
    const disciplines = currentPlanDisciplines.value
    
    if (disciplines && Array.isArray(disciplines)) {
      disciplines.forEach(discipline => {
        if (discipline && discipline.newdisid) {
          disciplinesMap.value[discipline.newdisid] = discipline
        }
      })
    }   
    
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: `Ошибка загрузки дисциплин: ${error.message}`,
      position: 'top-right'
    })
  }
}

async function onRowClick(row) {
  if (row.type !== 'discipline') {
    return
  }
  
  if (!currentPlanId.value) {
    $q.notify({
      type: 'warning',
      message: 'План не выбран. Пожалуйста, выберите учебный план.',
      position: 'top-right'
    })
    return
  }
  
  const disciplines = currentPlanDisciplines.value
  
  if (!disciplines || disciplines.length === 0) {
    await loadDisciplines()
  }
  
  if (Object.keys(disciplinesMap.value).length === 0) {
    disciplines.forEach(discipline => {
      if (discipline && discipline.newdisid) {
        disciplinesMap.value[discipline.newdisid] = discipline
      }
    })
  }
  
  let discipline = disciplinesMap.value[row.index]
  
  if (!discipline) {
    const found = disciplines?.find(
      disc => disc.newdisid === row.index
    )
    
    if (found) {
      discipline = found
      disciplinesMap.value[row.index] = found 
    }
  }
  
  if (!discipline) {
    $q.notify({
      type: 'warning',
      message: `Дисциплина "${row.index}" не найдена в списке дисциплин плана`,
      position: 'top-right'
    })
    return
  }
  
  if (!discipline.id) {
    $q.notify({
      type: 'warning',
      message: `Дисциплина "${row.index}" не имеет идентификатора`,
      position: 'top-right'
    })
    return
  }
  
  editingRow.value = {
    id: discipline.id,
    index: discipline.newdisid,
    name: discipline.dis
  }
  
  showEditor.value = true
}

function onCompetencesSaved() {
  showEditor.value = false
  editingRow.value = null
  
  $q.notify({
    type: 'positive',
    message: 'Компетенции успешно обновлены',
    position: 'top-right',
    timeout: 2000
  })
  
  // После сохранения запускаем проверку матрицы
  setTimeout(() => {
    loadCompetenceMatrix()
    loadDisciplines()
    runMatrixValidation()
  }, 500)
}

async function loadCompetenceMatrix() {
  matrixLoading.value = true
  try {
    const planId = currentPlanId.value
    
    if (!planId) {
      return
    }
    
    const response = await store.fetchCompetenceMatrix(planId)
    currentPlan.value = {
      planname: response.plan_name,
      abbrprofile: response.abbrprofile
    }
    
    const allItems = competenceMatrix.value
    allItems.forEach(item => {
      if (item.type === 'group' && item.level <= 2 && hasChildren(item.index)) {
        expandedGroups.value.add(item.index)
      }
    })
    
    await loadDisciplines()
    await runMatrixValidation()
    
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: `Ошибка загрузки матрицы: ${error.message}`,
      position: 'top-right'
    })
  } finally {
    matrixLoading.value = false
  }
}

watch(() => currentPlanId.value, (newPlanId) => {
  if (newPlanId) {
    disciplinesMap.value = {}
    store.resetMatrixValidation()
    loadCompetenceMatrix()
  }
})

onMounted(() => {
  if (currentPlanId.value) {
    loadCompetenceMatrix()
  }
})

onUnmounted(() => {
  highlightedDiscipline.value = null
})
</script>

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
  animation: highlight-pulse 2s ease-in-out;
  background-color: rgba(255, 193, 7, 0.15) !important;
  border: 2px solid #ffc107 !important;
  position: relative;

}

.blink-animation {
  animation: blink 1s 3;
}

@keyframes highlight-pulse {
  0% { background-color: rgba(255, 193, 7, 0.1); }
  50% { background-color: rgba(255, 193, 7, 0.3); }
  100% { background-color: rgba(255, 193, 7, 0.15); }
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.competence-indices-cell {
  max-height: 200px;
  overflow-y: auto;
  padding: 8px;
  word-break: break-word;
}

.text-italic {
  font-style: italic;
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
.discipline-type {
  font-weight: normal !important;
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

.rotate-180 {
  transform: rotate(180deg);
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
  
  .q-td {
    padding: 8px 16px;
  }
}

:deep(table) {
  table-layout: fixed;
  width: 100%;
  
  th, td {
    text-overflow: ellipsis;
    white-space: normal;
  }
  
  td:nth-child(1) { 
    width: 180px;
  }
  
  td:nth-child(2) {
    width: 400px;
  }
  
  td:nth-child(3) { 
    width: auto; 
  }
}

.has-validation-errors {
  :deep(.row-without-competences) {
    animation: error-pulse 2s infinite;
  }
}

@keyframes error-pulse {
  0%, 100% { 
    background-color: rgba(244, 67, 54, 0.08); 
  }
  50% { 
    background-color: rgba(244, 67, 54, 0.15); 
  }
}
</style>