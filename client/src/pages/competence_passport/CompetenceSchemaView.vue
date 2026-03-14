<script setup lang="ts">
import { ref, computed, onBeforeMount, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useQuasar, date } from 'quasar'
import { useCompetencePassportStore } from 'src/stores/competencePassportStore'
import { storeToRefs } from 'pinia'
import SchemaEditor from './components/SchemaEditor.vue'

const route = useRoute()
const $q = useQuasar()
const store = useCompetencePassportStore()

const {
  currentPlanId,
  schema,
  loading,
  schemaValidation,
  validatingSchema,
  maxSemesters,
  disciplines,
} = storeToRefs(store)

const showValidationErrors = ref(false)
const showEditor = ref(false)
const editingData = ref<any>(null)
const searchFilter = ref('')

const exporting = ref(false)

async function exportSchema() {
  exporting.value = true
  try {
    store.getSchemaReport()    
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

// Столбцы таблицы ошибок
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
    field: (row: any) => `${row.discipline_index} - ${row.discipline_name}`,
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

const formDisplayMap: Record<string, string> = {
  'ekz': 'Э',
  'zach': 'З',  
  'zacho': 'Зо',
  'kp': 'КП',
  'kr': 'КР'
}

function getFormDisplay(formControl: string[]){
  return formControl.map(form => formDisplayMap[form] || form).join(', ')
}

const validationStatus = computed(() => {
  if (validatingSchema.value) {
    return {
      type: 'info',
      title: 'Проверка схемы...',
      message: 'Идет проверка соответствия форм аттестации и индикаторов компетенций',
      details: false
    }
  }

  if (schemaValidation.value?.is_valid) {
    return {
      type: 'success',
      title: 'Схема компетенций проверена успешно!',
      message: 'Все формы аттестации соответствуют индикаторам компетенций.',
      details: true
    }
  }

  if (schemaValidation.value?.errors?.length > 0) {
    return {
      type: 'error',
      title: 'Найдены несоответствия в схеме компетенций',
      message: `Число форм аттестации не совпадает с числом индикаторов в ${schemaValidation.value.errors.length} случаях`,
      details: true
    }
  }

  return null
})

const lastCheckedFormatted = computed(() => {
  if (!schemaValidation.value?.checked_at) return 'еще не проверялась'
  return date.formatDate(schemaValidation.value.checked_at, 'DD.MM.YYYY HH:mm:ss')
})

const courseHeaders = computed(() => {
  const maxCourse = Math.ceil(maxSemesters.value / 2)
  return Array.from({ length: maxCourse }, (_, i) => i + 1)
})

const semesterHeaders = computed(() => {
  return Array.from({ length: maxSemesters.value }, (_, i) => i + 1)
})

function getSemesterData(discipline: any, semester: number) {
  return discipline.semester_data.find((s: any) => s.semester === semester)
}

// Фильтрация 
const filteredSchema = computed(() => {
  if (!searchFilter.value.trim()) {
    return schema.value
  }

  const term = (searchFilter.value || '').toLowerCase().trim()
  const visibleCompetences = new Set<string>()

  schema.value.forEach(item => {
    const matchesCompetence = 
      item.competence_index.toLowerCase().includes(term) ||
      item.competence.toLowerCase().includes(term)

    const matchingDisciplines = item.discipline_list.filter(disc =>
      disc.discipline_index.toLowerCase().includes(term) ||
      disc.discipline_name.toLowerCase().includes(term)
    )

    if (matchesCompetence || matchingDisciplines.length > 0) {
      visibleCompetences.add(item.competence_index)
    }
  })

  return schema.value.filter(item => visibleCompetences.has(item.competence_index))
})

async function loadSchemaData() {
  await store.fetchSchema(currentPlanId.value)
}

async function runSchemaValidation() {
  await store.validateSchemeIndicators()

}

function openEditDialog(discipline, competenceIndex, competenceName, semester) {
  const semesterData = discipline.semester_data?.find((s: any) => s.semester === semester) || {}

  const forms = {
    ekz: semesterData?.form_control?.includes('ekz') || false,
    zach: semesterData?.form_control?.includes('zach') || false,
    zacho: semesterData?.form_control?.includes('zacho') || false,
    kp: semesterData?.form_control?.includes('kp') || false,
    kr: semesterData?.form_control?.includes('kr') || false
  }
  
  editingData.value = {
    discipline_id: discipline.discipline_id,
    discipline_index: discipline.discipline_index,
    discipline_name: discipline.discipline_name,
    competence_index: competenceIndex,
    competence: competenceName,
    semester: semester,
    forms: forms,
    planId: currentPlanId.value
  }
  showEditor.value = true
}

function handleFormsSaved() {
  showEditor.value = false
  loadSchemaData()
}

function hasSemesterError(disciplineId, competenceIndex, semester) {
  return schemaValidation.value?.errors?.some(
    error => 
      error.discipline_id === disciplineId && 
      error.competence_index === competenceIndex && 
      error.semester === semester
  ) || false
}

function getSemesterCellClass(disciplineId, competenceIndex, semester) {
  return hasSemesterError(disciplineId, competenceIndex, semester) ? 'error-highlight' : ''
}

// Проверка наличия ошибок у дисциплины
function hasValidationError(disciplineId: number, competenceIndex: string) {
  return schemaValidation.value?.errors?.some(
    error => 
      error.discipline_id === disciplineId && 
      error.competence_index === competenceIndex
  ) || false
}

function navigateToFix(errorRow) {
  const competence = schema.value.find(c => c.competence_index === errorRow.competence_index)
  if (competence) {
    //const discipline = competence.discipline_list.find(d => d.discipline_id === errorRow.discipline_id)
    const discipline = disciplines.value.find(d => d.discipline_id === errorRow.discipline_id)
    if (discipline) {
      //openEditDialog(discipline, errorRow.competence_index, errorRow.competence_name, errorRow.semester)
      openEditDialog(
        {
          discipline_id: discipline.discipline_id,
          discipline_index: discipline.discipline_index,
          discipline_name: discipline.discipline_name,
          semester_data: [] // пусто, т.к. форм может не быть
        },
        errorRow.competence_index,
        errorRow.competence_name,
        errorRow.semester
      )
      return
    }
  }
  $q.notify({ 
    type: 'warning', 
    position: 'top-right', 
    message: 'Дисциплина не найдена в текущей схеме' 
  })
}

async function navigateToPassport(errorRow) {
  try {
    const result = await store.fixSchemeIndicators(
      errorRow.discipline_id,
      errorRow.competence_index,
      errorRow.scheme_forms_count,
      errorRow.indicators_count
    )
    
    if (result.success) {
      $q.notify({ type: 'positive', position: 'top-right', message: result.message, timeout: 5000 })
    }
  } catch (error) {
    $q.notify({ type: 'warning', position: 'top-right', message: 'Не удалось автоматически скорректировать индикаторы' })
  }
}

onBeforeMount(() => {
  loadSchemaData()
  runSchemaValidation()
})

watch(() => route.params.id, () => {
  loadSchemaData()
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
            :label="showValidationErrors ? 'Скрыть детали' : 'Показать детали'" 
            @click="showValidationErrors = !showValidationErrors"
            class="q-mr-sm"
          />
          <q-btn 
            v-if="validationStatus.type === 'error'"
            flat 
            :color="validationStatus.type === 'error' ? 'white' : 'dark'" 
            label="Обновить проверку" 
            @click="runSchemaValidation()"
            :loading="validatingSchema"
            icon="refresh"
          />
        </template>
      </q-banner>
      
      <q-slide-transition>
        <div v-if="showValidationErrors && schemaValidation?.errors?.length" class="validation-details q-pa-md bg-grey-2 q-mt-sm">
          <q-card class="q-mb-md">
            <q-card-section class="q-pa-none">
              <q-table
                :rows="schemaValidation.errors"
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
                        :loading="validatingSchema"
                      />
                      <q-btn
                        size="sm"
                        color="primary"
                        label="Исправить в паспорте"
                        @click="navigateToPassport(props.row)"
                        title="Изменить число индикаторов"
                        :loading="store.saving"
                      />
                    </div>
                  </q-td>
                </template>
              </q-table>
            </q-card-section>
          </q-card>

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
        <h2 class="text-h4 q-ma-none">Схема компетенций</h2>
        <div class="text-subtitle1 text-grey">
          Соответствие компетенций, дисциплины и семестров изучения
        </div>
        <div class="text-subtitle1 text-grey">
          Окно редактора вызывается щелчком мыши в необходимой ячейке
        </div>
      </div>
      
      <div class="col-auto">
        <div class="row items-center q-gutter-md q-mb-md">
          <q-btn
            flat
            dense
            color="primary"
            icon="check_circle"
            label="Проверить"
            @click="runSchemaValidation()"
            :loading="validatingSchema"
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
            @clear="searchFilter = ''"
            style="min-width: 250px;"
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
            @click="exportSchema"
            :loading="exporting"
            class="q-mr-sm q-pr-sm bg-primary text-white"
          >
            <q-tooltip>Скачать схему формирования компетенций в формате Word</q-tooltip>
          </q-btn>
        </div>
      </div>
    </div>

    <!-- Таблица схемы -->
    <div class="competence-schema-table-container q-mb-lg">
      <table class="q-table" >
        <thead>
          <tr>
            <th rowspan="2" class="bg-grey-2">
              <div class="text-weight-bold">Код дисциплины</div>
            </th>
            <th rowspan="2" class="bg-grey-2">
              <div class="text-weight-bold">Наименование дисциплины</div>
            </th>
            <!-- <th colspan="2" class="course-1-header">
              <div class="text-weight-bold">1 курс</div>
            </th>
            <th colspan="2" class="course-2-header">
              <div class="text-weight-bold">2 курс</div>
            </th>
            <th colspan="2" class="course-3-header">
              <div class="text-weight-bold">3 курс</div>
            </th>
            <th colspan="2" class="course-4-header">
              <div class="text-weight-bold">4 курс</div>
            </th> -->

            <th 
              v-for="course in courseHeaders" 
              :key="course"
              :colspan="2"
              :class="`course-${course}-header`"
            >
              <div class="text-weight-bold">{{ course }} курс</div>
            </th>
          </tr>
          <tr>
            <!-- <th class="semester-header semester-1">1 сем</th>
            <th class="semester-header semester-2">2 сем</th>
            <th class="semester-header semester-3">3 сем</th>
            <th class="semester-header semester-4">4 сем</th>
            <th class="semester-header semester-5">5 сем</th>
            <th class="semester-header semester-6">6 сем</th>
            <th class="semester-header semester-7">7 сем</th>
            <th class="semester-header semester-8">8 сем</th> -->
            <th 
              v-for="semester in semesterHeaders" 
              :key="semester"
              :class="`semester-header semester-${semester}`"
            >
              {{ semester }} сем
            </th>
          </tr>
        </thead>
        
        <tbody>
          <template v-for="competence in filteredSchema" :key="competence.competence_index">
            <!-- Строка компетенции -->
            <tr class="competence-row">
              <td :colspan="2 + semesterHeaders.length">
                <div class="text-center q-pa-sm">
                  <div class="text-weight-bold text-primary text-h6">
                    {{ competence.competence_index }}
                  </div>
                  <div class="text-caption q-mt-xs">
                    {{ competence.competence }}
                  </div>
                </div>
              </td>
            </tr>
            
            <!-- Строки дисциплин -->
            <tr 
              v-for="discipline in competence.discipline_list" 
              :key="`${competence.competence_index}-${discipline.discipline_id}`"
              class="discipline-row"
              :class="{ 
                'bg-grey-1': (competence.discipline_list.indexOf(discipline) % 2 === 0),
                'row-with-error': hasValidationError(discipline.discipline_id, competence.competence_index)
              }"
            >
              <td class="text-center" style="font-weight: 500;">
                {{ discipline.discipline_index }}
              </td>
              <td class="text-wrap" style="max-width: 320px; text-align: left;">
                {{ discipline.discipline_name }}
              </td>
              <td 
                v-for="semester in semesterHeaders" 
                :key="semester" 
                :class="getSemesterCellClass(discipline.discipline_id, competence.competence_index, semester)"
                @click="openEditDialog(discipline, competence.competence_index, competence.competence, semester)"
                style="cursor: pointer; position: relative;"
              >
                <div class="text-center">
                  <div v-if="getSemesterData(discipline, semester)">
                    <div class="semester-forms text-weight-medium" style="font-size: 0.9rem;">
                      {{ getFormDisplay(getSemesterData(discipline, semester)?.form_control || []) }}
                    </div>
                    <q-icon 
                      v-if="hasSemesterError(discipline.discipline_id, competence.competence_index, semester)"
                      name="error" 
                      color="negative" 
                      size="12px"
                      class="absolute-top-right q-ma-xs"
                    />
                  </div>
                </div>
              </td>
            </tr>
          </template>
          
          <tr v-if="filteredSchema.length === 0 && !loading">
            <td :colspan="2 + semesterHeaders.length" class="text-center q-py-xl">
              <div class="full-width row flex-center q-gutter-sm">
                <q-icon name="info" size="2em" color="grey" />
                <span>Нет данных для отображения. Проверьте матрицу компетенций.</span>
              </div>
            </td>
          </tr>
          
          <tr v-if="loading">
            <td :colspan="2 + semesterHeaders.length" class="text-center q-py-xl">
              <div class="full-width row flex-center q-gutter-sm">
                <q-spinner color="primary" size="2em" />
                <span>Загрузка данных схемы...</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Редактор -->
    <SchemaEditor
      v-model="showEditor"
      :editing-data="editingData"
      @saved="handleFormsSaved"
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

.competence-schema-table-container {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: visible;
}

.q-table {
  width: 100%;
  border-collapse: collapse;
  
  th, td {
    border: 1px solid #e0e0e0;
    padding: 8px;
    text-align: center;
    vertical-align: middle;
    font-size: 0.85rem;
  }

  thead th {
    position: sticky;
    z-index: 10;
    background: white;
    outline: 1px solid #e0e0e0;
  }

  thead tr:first-child th {
    top: 64px;
  }
  thead tr:nth-child(2) th {
    top: calc(64px + 48px); 
  }

  thead th.bg-grey-2 {
    background-color: #f5f5f5 !important;
  }

  thead th.course-1-header { background-color: #e8f5e9 !important; }
  thead th.course-2-header { background-color: #e3f2fd !important; }
  thead th.course-3-header { background-color: #fff3e0 !important; }
  thead th.course-4-header { background-color: #fce4ec !important; }
  thead th.course-5-header { background-color: #f3e5f5 !important; }
  thead th.course-6-header { background-color: #e8eaf6 !important; }

  thead th.semester-1,
  thead th.semester-2 { background-color: #e8f5e9 !important; }

  thead th.semester-3,
  thead th.semester-4 { background-color: #e3f2fd !important; }

  thead th.semester-5,
  thead th.semester-6 { background-color: #fff3e0 !important; }

  thead th.semester-7,
  thead th.semester-8 { background-color: #fce4ec !important; }

  thead th.semester-9,
  thead th.semester-10 { background-color: #f3e5f5 !important; }

  thead th.semester-11,
  thead th.semester-12 { background-color: #e8eaf6 !important; }

  td {
    border-bottom: 1px solid rgba(0,0,0,0.05);
    
    .semester-forms {
      font-size: 0.9rem;
      font-weight: 500;
      line-height: 1.2;
      color: #333;
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

  .row-with-error {
    background-color: rgba(244, 67, 54, 0.071) !important;
    border-left: 4px solid #f44336 !important;
    
    &:hover {
      background-color: rgba(244, 67, 54, 0.088) !important;
    }
  }

  .error-highlight {
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

</style>