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

        <!-- Таблица схемы компетенций -->
        <div class="competence-schema-table-container q-mb-lg">
          <table class="q-table">
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
                <tr v-else-if="row.type === 'discipline'" class="discipline-row" :class="{ 'bg-grey-1': index % 2 === 0 }">
                  <td class="text-center" style="font-weight: 500;">
                    {{ row.discipline_index }}
                  </td>
                  <td class="text-wrap" style="max-width: 320px; text-align: left;">
                    {{ row.discipline_name }}
                  </td>
                  <td 
                    v-for="semester in [1,2,3,4,5,6,7,8]" 
                    :key="semester" 
                    :class="`semester-${semester}`"
                    @click="openEditDialog(row, semester)"
                    style="cursor: pointer; position: relative;"
                  >
                    <div class="text-center">
                      <div v-if="row[`semester_${semester}`] && row[`semester_${semester}`] !== ''">
                        <div class="semester-forms text-weight-medium" style="font-size: 0.9rem;">
                          {{ row[`semester_${semester}`].forms_display }}
                        </div>
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
import { useQuasar } from 'quasar'
import { storeToRefs } from 'pinia'

const $q = useQuasar()
const router = useRouter()
const store = useCompetencePassportStore()

const {
  schemaData,
  schemaLoading,
  currentPlanId
} = storeToRefs(store)


const searchFilter = ref('')
const editDialogVisible = ref(false)
const editingData = ref({})

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

const competenceCount = computed(() => {
  return (schemaData.value || []).filter(row => row.type === 'competence').length
})

const disciplineCount = computed(() => {
  return (schemaData.value|| []).filter(row => row.type === 'discipline').length
})

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
}

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
.competence-schema-table-container {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  overflow: hidden;
  background: white;
  max-width: 100%;
  overflow-x: auto;
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