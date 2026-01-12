<template>
  <top-navigation-menu>
    <template #content>
      <div class="q-pa-md q-mb-lg">
        <div class="row items-center q-mb-md">
          <div class="col">
            <h2 class="text-h4 q-ma-none">Схема компетенций</h2>
            <div class="text-subtitle1 text-grey">
              Соответствие компетенций, дисциплины и семестров изучения
            </div>
            <div class="text-subtitle1 text-grey">
              Окно редактора вызывается щелчком мыши в необходимой ячейке
            </div>
          </div>
          
          <div class="col-auto">
            <div class="row items-center q-gutter-md">
              <!-- Кнопка проверки -->
              <q-btn
                flat
                dense
                color="primary"
                icon="check_circle"
                label="Проверить"
                @click="validateScheme"
                :loading="validationLoading"
                class="q-mr-sm"
              >
                <q-tooltip>Проверить соответствие форм аттестации и индикаторов компетенций</q-tooltip>
              </q-btn>
              
              <q-input
                v-model="searchFilter"
                placeholder="Поиск по компетенциям, дисциплинам..."
                dense
                outlined
                clearable
                style="min-width: 250px;"
              >
                <template v-slot:append>
                  <q-icon name="search" />
                </template>
              </q-input>
            </div>
          </div>
        </div>

        <!-- Блок с валидацией схемы -->
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
                :label="showValidationErrors ? 'Скрыть детали' : 'Показать детали'" 
                @click="showValidationErrors = !showValidationErrors"
                class="q-mr-sm"
              />
              <q-btn 
                v-if="validationStatus.type === 'error'"
                flat 
                :color="validationStatus.type === 'error' ? 'white' : 'dark'" 
                label="Обновить проверку" 
                @click="validateScheme"
                :loading="validationLoading"
                icon="refresh"
              />
            </template>
          </q-banner>
          
          <!-- Детали валидации -->
          <q-slide-transition>
            <div v-if="showValidationErrors && validationErrors.length > 0" class="validation-details q-pa-md bg-grey-2 q-mt-sm">
              <!-- Таблица с ошибками -->
              <q-card class="q-mb-md">
                <q-card-section class="q-pa-none">
                  <q-table
                    :rows="validationErrors"
                    :columns="validationColumns"
                    row-key="id"
                    dense
                    flat
                    bordered
                  >
                    <template v-slot:body-cell-actions="props">
                      <q-td :props="props">
                        <div class="column items-center q-gutter-y-xs">
                          <q-btn
                            size="sm"
                            color="primary"
                            label="Исправить в схеме"
                            @click="navigateToFix(props.row)"
                            title="Изменить формы аттестации"
                            :loading="validationLoading"
                          />
                          <q-btn
                            size="sm"
                            color="primary"
                            label="Исправить в паспорте"
                            @click="navigateToPassport(props.row)"
                            title="Изменить число индикаторов"
                            :loading="fixingIndicatorsLoading"
                          />
                        </div>
                      </q-td>
                    </template>
                  </q-table>
                </q-card-section>
              </q-card>
              
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

        <!-- Таблица схемы компетенций -->
        <div class="competence-schema-table-container q-mb-lg">
          <table class="q-table" :class="{ 'has-validation-errors': validationErrors.length > 0 }">
            <thead>
              <!-- Первая строка заголовков -->
              <tr>
                <th rowspan="2" class="bg-grey-2" style="width: 80px; min-width: 80px;">
                  <div class="text-weight-bold">Код дисциплины</div>
                </th>
                <th rowspan="2" class="bg-grey-2" style="width: 320px; min-width: 320px;">
                  <div class="text-weight-bold">Наименование дисциплины</div>
                </th>
                <th colspan="2" class="course-1-header" style="width: 140px; min-width: 140px;">
                  <div class="text-weight-bold">1 курс</div>
                </th>
                <th colspan="2" class="course-2-header" style="width: 140px; min-width: 140px;">
                  <div class="text-weight-bold">2 курс</div>
                </th>
                <th colspan="2" class="course-3-header" style="width: 140px; min-width: 140px;">
                  <div class="text-weight-bold">3 курс</div>
                </th>
                <th colspan="2" class="course-4-header" style="width: 140px; min-width: 140px;">
                  <div class="text-weight-bold">4 курс</div>
                </th>
              </tr>
              
              <!-- Вторая строка заголовков - семестры -->
              <tr>
                <th class="semester-header semester-1">1 сем</th>
                <th class="semester-header semester-2">2 сем</th>
                <th class="semester-header semester-3">3 сем</th>
                <th class="semester-header semester-4">4 сем</th>
                <th class="semester-header semester-5">5 сем</th>
                <th class="semester-header semester-6">6 сем</th>
                <th class="semester-header semester-7">7 сем</th>
                <th class="semester-header semester-8">8 сем</th>
              </tr>
            </thead>
            
            <tbody>
              <template v-for="(row, index) in visibleRows" :key="row.id">
                <!-- Строка компетенции -->
                <tr v-if="row.type === 'competence'" class="competence-row">
                  <td :colspan="10">
                    <div class="text-center q-pa-sm">
                      <div class="text-weight-bold text-primary text-h6">
                        {{ row.competence_index }}
                      </div>
                      <div class="text-caption q-mt-xs">
                        {{ row.competence_name }}
                      </div>
                    </div>
                  </td>
                </tr>
                
                <!-- Строка дисциплины -->
                <tr v-else-if="row.type === 'discipline'" class="discipline-row" :class="{ 
                  'bg-grey-1': index % 2 === 0,
                  'row-with-error': hasValidationError(row)
                }" :data-id="row.discipline_id" :data-competence="row.parent_competence">
                  <td class="text-center" style="font-weight: 500;">
                    {{ row.discipline_index }}
                  </td>
                  <td class="text-wrap" style="max-width: 320px; text-align: left;">
                    {{ row.discipline_name }}
                  </td>
                  <td 
                    v-for="semester in [1,2,3,4,5,6,7,8]" 
                    :key="semester" 
                    :class="`semester-${semester} ${getSemesterCellClass(row, semester)}`"
                    @click="openEditDialog(row, semester)"
                    style="cursor: pointer; position: relative;"
                  >
                    <div class="text-center">
                      <div v-if="row[`semester_${semester}`] && row[`semester_${semester}`] !== ''">
                        <div class="semester-forms text-weight-medium" style="font-size: 0.9rem;">
                          {{ row[`semester_${semester}`].forms_display }}
                        </div>
                        <q-icon 
                          v-if="hasSemesterError(row.discipline_id, row.parent_competence, semester)"
                          name="error" 
                          color="negative" 
                          size="12px"
                          class="absolute-top-right q-ma-xs"
                        />
                      </div>
                      <div v-else class="text-grey-6 text-caption">
                        <q-icon name="edit" size="xs" />
                      </div>
                    </div>
                  </td>
                </tr>
                
                <tr v-else-if="row.type === 'divider'" class="divider-row">
                  <td :colspan="10" style="background-color: #fff3cd; font-weight: bold; border-top: 2px solid #ffeaa7; border-bottom: 2px solid #ffeaa7;">
                    <div class="text-center text-warning q-py-xs">
                      <q-icon name="warning" class="q-mr-sm" />
                      {{ row.label }}
                    </div>
                  </td>
                </tr>
              </template>

              <tr v-if="visibleRows.length === 0 && !schemaLoading">
                <td :colspan="10" class="text-center q-py-xl">
                  <div class="full-width row flex-center q-gutter-sm">
                    <q-icon name="info" size="2em" color="grey" />
                    <span>Нет данных для отображения. Проверьте матрицу компетенций.</span>
                  </div>
                </td>
              </tr>
              
              <tr v-if="schemaLoading">
                <td :colspan="10" class="text-center q-py-xl">
                  <div class="full-width row flex-center q-gutter-sm">
                    <q-spinner color="primary" size="2em" />
                    <span>Загрузка данных схемы...</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <edit-semester-forms-dialog
          v-model="editDialogVisible"
          :editing-data="editingData"
          @saved="handleFormsSaved"
        />
      </div>
    </template>
  </top-navigation-menu>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useCompetencePassportStore } from 'stores/competencePassportStore'
import { useRouter } from 'vue-router'
import TopNavigationMenu from './components/TopNavigationMenu.vue'
import EditSemesterFormsDialog from './components/EditSemesterFormsDialog.vue'
import { useQuasar, date } from 'quasar'
import { storeToRefs } from 'pinia'

const $q = useQuasar()
const router = useRouter()
const store = useCompetencePassportStore()

const {
  schemaData,
  schemaLoading,
  currentPlanId,
  validationErrors,
  validationLoading
} = storeToRefs(store)
const showValidationErrors = ref(false)
const lastChecked = ref(null)
const fixingIndicatorsLoading = ref(false)

const validationColumns = [
  {
    name: 'competence_index',
    label: 'Код компетенции',
    field: 'competence_index',
    align: 'left',
    sortable: true
  },
  {
    name: 'discipline',
    label: 'Дисциплина',
    field: row => `${row.discipline_index} - ${row.discipline_name}`,
    align: 'left',
    sortable: true
  },
  {
    name: 'semester',
    label: 'Семестр',
    field: 'semester',
    align: 'center',
    sortable: true
  },
  {
    name: 'message',
    label: 'Ошибка',
    field: 'message',
    align: 'left',
    sortable: true
  },
  {
    name: 'actions',
    label: 'Действия',
    align: 'center'
  }
]

const searchFilter = ref('')
const editDialogVisible = ref(false)
const editingData = ref({})

// Статус валидации
const validationStatus = computed(() => {
  if (validationLoading.value) {
    return {
      type: 'info',
      title: 'Проверка схемы...',
      message: 'Идет проверка соответствия форм аттестации и индикаторов компетенций',
      details: false
    }
  }
  
  if (validationErrors.value.length === 0 && lastChecked.value) {
    return {
      type: 'success',
      title: 'Схема компетенций проверена успешно!',
      message: 'Все формы аттестации соответствуют индикаторам компетенций.',
      details: true
    }
  } else if (validationErrors.value.length > 0) {
    return {
      type: 'error',
      title: 'Найдены несоответствия в схеме компетенций',
      message: `Число форм аттестации не совпадает с числом индикаторов в ${validationErrors.value.length} случаях`,
      details: true
    }
  }
  
  return null
})

const lastCheckedFormatted = computed(() => {
  if (!lastChecked.value) return 'еще не проверялась'
  
  const timeStamp = date.formatDate(
    lastChecked.value, 
    'DD.MM.YYYY HH:mm:ss'
  )
  
  return timeStamp
})

const filteredRows = computed(() => {
  if (!searchFilter.value) {
    return schemaData.value || []
  }
  
  const searchLower = searchFilter.value.toLowerCase()
  const rows = schemaData.value || []
  const result = []
  
  const foundCompetences = new Set()
  const foundDisciplines = new Map()

  rows.forEach(row => {
    if (row.type === 'competence') {
      if (row.competence_index.toLowerCase().includes(searchLower) ||
          row.competence_name.toLowerCase().includes(searchLower)) {
        foundCompetences.add(row.competence_index)
      }
    } else if (row.type === 'discipline') {
      if ((row.discipline_index && row.discipline_index.toLowerCase().includes(searchLower)) ||
          (row.discipline_name && row.discipline_name.toLowerCase().includes(searchLower))) {
        const compKey = row.parent_competence
        if (!foundDisciplines.has(compKey)) {
          foundDisciplines.set(compKey, [])
        }
        foundDisciplines.get(compKey).push(row)
        
        if (compKey) {
          foundCompetences.add(compKey)
        }
      }
    }
  })
  
  rows.forEach(row => {
    if (row.type === 'competence') {
      const compIndex = row.competence_index
      if (foundCompetences.has(compIndex)) {
        result.push(row)
      }
    } else if (row.type === 'discipline') {
      const compIndex = row.parent_competence

      if (foundDisciplines.has(compIndex) && 
          foundDisciplines.get(compIndex).some(d => d.discipline_id === row.discipline_id)) {
        result.push(row)
      } else if (foundCompetences.has(compIndex) && 
                !foundDisciplines.has(compIndex)) {
        result.push(row)
      }
    } else if (row.type === 'divider') {
      if (result.length > 0) {
        result.push(row)
      }
    }
  })
  
  return result
})

const visibleRows = computed(() => {
  return filteredRows.value
})

// Проверка наличия ошибок для строки дисциплины
function hasValidationError(row) {
  return validationErrors.value.some(error => 
    error.discipline_id === row.discipline_id && 
    error.competence_index === row.parent_competence
  )
}

function hasSemesterError(disciplineId, competenceIndex, semester) {
  return validationErrors.value.some(error => 
    error.discipline_id === disciplineId && 
    error.competence_index === competenceIndex &&
    error.semester === semester
  )
}

function getSemesterCellClass(row, semester) {
  if (hasSemesterError(row.discipline_id, row.parent_competence, semester)) {
    return 'error-highlight'
  }
  return ''
}

async function loadCompetenceSchema() {
  try {
    if (!currentPlanId.value) {
      throw new Error('План не выбран')
    }
    
    await store.fetchCompetenceSchema(currentPlanId.value)
    
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: `Ошибка загрузки схемы компетенций: ${error.message}`,
      position: 'top-right'
    })
  }
}

function openEditDialog(row, semester) {
  editingData.value = {
    discipline_id: row.discipline_id,
    discipline_index: row.discipline_index,
    discipline_name: row.discipline_name,
    competence_index: row.parent_competence,
    competence: getCompetenceName(row.parent_competence),
    semester: semester,
    forms: row[`semester_${semester}`]?.forms || [],
    planId: currentPlanId.value
  }
  
  editDialogVisible.value = true
}

function getCompetenceName(competenceIndex) {
  const currentSchemaData = schemaData.value || []
  const competence = currentSchemaData.find(item => 
    item.type === 'competence' && item.competence_index === competenceIndex
  )
  return competence ? competence.competence_name : ''
}

function handleFormsSaved() {
  loadCompetenceSchema()
  validateScheme()
}

async function validateScheme() {
  try {
    if (!currentPlanId.value) {
      $q.notify({
        type: 'warning',
        message: 'Сначала выберите учебный план',
        position: 'top-right'
      })
      return
    }
    
    validationLoading.value = true
    const result = await store.validateSchemeIndicators(currentPlanId.value)
    lastChecked.value = new Date()
    
    if (result.hasErrors) {
      validationErrors.value = result.errors
      showValidationErrors.value = true
    } else {
      validationErrors.value = []
      $q.notify({
        type: 'positive',
        message: 'Проверка пройдена успешно! Несоответствий не найдено.',
        position: 'top-right',
        timeout: 3000
      })
    }
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: `Ошибка при проверке: ${error.message}`,
      position: 'top-right'
    })
  } finally {
    validationLoading.value = false
  }
}

// Методы навигации для исправления
function navigateToFix(errorRow) {
  const rows = schemaData.value || []
  const disciplineRow = rows.find(row => 
    row.type === 'discipline' && 
    row.discipline_id === errorRow.discipline_id &&
    row.parent_competence === errorRow.competence_index
  )
  
  if (disciplineRow) {
    openEditDialog(disciplineRow, errorRow.semester)
  } else {
    $q.notify({
      type: 'warning',
      message: 'Дисциплина не найдена в текущей схеме',
      position: 'top-right'
    })
  }
}

async function navigateToPassport(errorRow) {
  try {
    fixingIndicatorsLoading.value = true

    const rows = schemaData.value || []
    const disciplineRow = rows.find(row => 
      row.type === 'discipline' && 
      row.discipline_id === errorRow.discipline_id &&
      row.parent_competence === errorRow.competence_index
    )
    
    if (!disciplineRow) {
      throw new Error('Дисциплина не найдена в текущей схеме')
    }
    
    const result = await store.fixSchemeIndicators({
      plan_id: currentPlanId.value,
      discipline_id: errorRow.discipline_id,
      competence_index: errorRow.competence_index,
      scheme_forms_count: errorRow.scheme_forms_count,
      indicators_count: errorRow.indicators_count,
      semester: errorRow.semester
    })
    
    if (result.success) {
      let message = 'Индикаторы успешно скорректированы: '
      const actions = []
      
      if (result.indicators_created > 0) {
        actions.push(`создано ${result.indicators_created} индикаторов`)
      }
      if (result.indicators_removed > 0) {
        actions.push(`удалено ${result.indicators_removed} индикаторов`)
      }
      
      $q.notify({
        type: 'positive',
        message: message,
        position: 'top-right',
        timeout: 5000
      })

      await loadCompetenceSchema()
      await validateScheme()

      router.push({
        name: 'competencePassport',
        query: {
          plan_id: currentPlanId.value,
          discipline_id: errorRow.discipline_id,
          highlight_competence: errorRow.competence_index
        }
      })
    } else {
      throw new Error(result.error || 'Не удалось скорректировать индикаторы')
    }
    
  } catch (error) {
    console.error('Error fixing indicators:', error)

    $q.notify({
      type: 'warning',
      message: `Не удалось автоматически скорректировать индикаторы: ${error.message}`,
      position: 'top-right',
      timeout: 5000
    })

    // router.push({
    //   name: 'competencePassport',
    //   query: {
    //     plan_id: currentPlanId.value,
    //     discipline_id: errorRow.discipline_id,
    //     highlight_competence: errorRow.competence_index
    //   }
    // })
  } finally {
    fixingIndicatorsLoading.value = false
  }
}

watch(() => store.validationErrors, (newErrors) => {
  validationErrors.value = newErrors
})

watch(() => schemaData.value, () => {
  if (schemaData.value && schemaData.value.length > 0) {
    validateScheme()
  }
})

watch(() => currentPlanId.value, (newPlanId) => {
  if (newPlanId) {
    loadCompetenceSchema()
  }
})

onMounted(() => {
  if (currentPlanId.value) {
    loadCompetenceSchema()
  } else {
    $q.notify({
      type: 'warning',
      message: 'Выберите учебный план для просмотра схемы компетенций',
      position: 'top-right'
    })
  }
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

.competence-schema-table-container {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  background: white;
  max-width: 100%;
  overflow-x: auto;
}

.row-with-error {
  background-color: rgba(244, 67, 54, 0.08) !important;
  border-left: 4px solid #f44336 !important;
  
  &:hover {
    background-color: rgba(244, 67, 54, 0.12) !important;
  }
}

.q-table {
  width: 100%;
  border-collapse: collapse;
  min-width: 900px;
  
  th, td {
    border: 1px solid #e0e0e0;
    padding: 8px;
    text-align: center;
    vertical-align: middle;
    font-size: 0.85rem;
  }
  
  th {
    background-color: #fafafa;
    font-weight: bold;
    
    &.bg-grey-2 {
      background-color: #f5f5f5 !important;
    }
    
    // Заголовки курсов
    &.course-1-header {
      background-color: #e8f5e9 !important;
      border-left: 2px solid #4caf50 !important;
    }
    
    &.course-2-header {
      background-color: #e3f2fd !important;
      border-left: 2px solid #2196f3 !important;
    }
    
    &.course-3-header {
      background-color: #fff3e0 !important;
      border-left: 2px solid #ff9800 !important;
    }
    
    &.course-4-header {
      background-color: #fce4ec !important;
      border-left: 2px solid #e91e63 !important;
    }
    
    // Заголовки семестров
    &.semester-header {
      font-weight: 500;
      font-size: 0.8rem;
      color: #666;
      border-bottom: 1px solid rgba(0,0,0,0.05);
    }
    
    &.semester-1,
    &.semester-2 {
      background-color: rgba(232, 245, 233, 0.3) !important;
    }
    
    &.semester-3,
    &.semester-4 {
      background-color: rgba(227, 242, 253, 0.3) !important;
    }
    
    &.semester-5,
    &.semester-6 {
      background-color: rgba(255, 243, 224, 0.3) !important;
    }
    
    &.semester-7,
    &.semester-8 {
      background-color: rgba(252, 228, 236, 0.3) !important;
    }
  }
  
  td {
    border-bottom: 1px solid rgba(0,0,0,0.05);
    
    &.text-wrap {
      word-wrap: break-word;
      word-break: break-word;
      overflow-wrap: break-word;
      white-space: normal;
      text-align: left;
      min-height: 40px;
      vertical-align: top;
      padding-top: 10px;
      padding-bottom: 10px;
    }
    
    &.semester-1,
    &.semester-2,
    &.semester-3,
    &.semester-4,
    &.semester-5,
    &.semester-6,
    &.semester-7,
    &.semester-8 {
      background-color: white !important;
    }
    
    .semester-forms {
      font-size: 0.9rem;
      font-weight: 500;
      line-height: 1.2;
      color: #333;
      padding: 2px 4px;
      border-radius: 4px;
      display: inline-block;
    }
  }
  
  .competence-row {
    td {
      padding: 12px !important;
      background-color: #e0f2f1;
      border-bottom: 2px solid #7abdb7;
    }
    
    .text-h6 {
      font-size: 1.1rem;
      font-weight: 600;
    }
  }
  
  .discipline-row {
    transition: background-color 0.2s;
    
    &:hover {
      background-color: #f5f5f5 !important;
    }
  }
  
  .divider-row {
    td {
      padding: 8px !important;
    }
  }
  
  .bg-grey-1 {
    background-color: #fafafa !important;
  }
  
  .error-highlight {
    position: relative;
    background-color: rgba(244, 67, 54, 0.15) !important;
    border: 1px solid rgba(244, 67, 54, 0.3) !important;
    
    .semester-forms {
      color: #f44336;
      font-weight: bold;
    }
  }
}

.absolute-top-right {
  position: absolute;
  top: 4px;
  right: 4px;
}

.has-validation-errors {
  .row-with-error {
    animation: error-pulse 2s infinite;
  }
  
  .error-highlight {
    animation: cell-pulse 2s infinite;
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

@keyframes cell-pulse {
  0%, 100% { 
    background-color: rgba(244, 67, 54, 0.15); 
  }
  50% { 
    background-color: rgba(244, 67, 54, 0.25); 
  }
}

@media (max-width: 1200px) {
  .competence-schema-table-container {
    overflow-x: auto;
  }
}

@media (max-width: 768px) {
  .competence-schema-table-container {
    border-radius: 4px;
  }
  
  .q-table {
    th, td {
      padding: 4px 6px;
    }
    
    td.text-wrap {
      max-width: 250px;
    }
    
    .semester-forms {
      font-size: 0.8rem;
    }
  }
}
</style>