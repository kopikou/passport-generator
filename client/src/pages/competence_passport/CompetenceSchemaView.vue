<template>
  <top-navigation-menu>
    <template #content>
      <div class="q-pa-md">
        <div class="row items-center q-mb-md">
          <div class="col">
            <h2 class="text-h4 q-ma-none">Схема компетенций</h2>
            <div class="text-subtitle1 text-grey">
              Соответствие компетенций, дисциплин и семестров изучения
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
        <div class="competence-schema-table-container">
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
              <template v-for="row in visibleRows" :key="row.id">
                <!-- Строка компетенции -->
                <tr v-if="row.type === 'competence'" class="competence-row">
                  <td :colspan="10" style="background-color: #e3f2fd; border-bottom: 2px solid #bbdefb;">
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
                <tr v-else-if="row.type === 'discipline'" class="discipline-row" :class="{ 'bg-grey-1': rowIndex % 2 === 0 }">
                  <td class="text-center" style="font-weight: 500;">
                    {{ row.discipline_index }}
                  </td>
                  <td class="text-truncate" style="max-width: 320px;">
                    {{ row.discipline_name }}
                  </td>
                  <td v-for="semester in [1,2,3,4,5,6,7,8]" :key="semester" :class="`semester-${semester}`">
                    <div class="text-center">
                      <div v-if="row[`semester_${semester}`] && row[`semester_${semester}`] !== ' '">
                        <q-chip
                          size="xs"
                          :color="getSemesterChipColor(row[`semester_${semester}`])"
                          text-color="white"
                          dense
                        >
                          {{ row[`semester_${semester}`] }}
                        </q-chip>
                      </div>
                    </div>
                  </td>
                </tr>
                
                <!-- Разделитель -->
                <tr v-else-if="row.type === 'divider'" class="divider-row">
                  <td :colspan="10" style="background-color: #fff3cd; font-weight: bold; border-top: 2px solid #ffeaa7; border-bottom: 2px solid #ffeaa7;">
                    <div class="text-center text-warning q-py-xs">
                      <q-icon name="warning" class="q-mr-sm" />
                      {{ row.label }}
                    </div>
                  </td>
                </tr>
              </template>
              
              <!-- Нет данных -->
              <tr v-if="visibleRows.length === 0">
                <td :colspan="10" class="text-center q-py-xl">
                  <div class="full-width row flex-center q-gutter-sm">
                    <q-icon name="info" size="2em" color="grey" />
                    <span>Нет данных для отображения. Проверьте матрицу компетенций.</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Статистика -->
        <div class="row q-mt-md">
          <div class="col">
            <div class="text-caption text-grey">
              Показано: {{ visibleRows.length }} строк ({{ competenceCount }} компетенций, {{ disciplineCount }} дисциплин)
            </div>
          </div>
        </div>
      </div>
    </template>
  </top-navigation-menu>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useCompetencePassportStore } from 'stores/competencePassportStore'
import { useRouter } from 'vue-router'
import TopNavigationMenu from './components/TopNavigationMenu.vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const router = useRouter()
const store = useCompetencePassportStore()

const loading = ref(false)
const searchFilter = ref('')
const schemaData = ref([])

// Вычисляемые свойства
const filteredRows = computed(() => {
  if (!searchFilter.value) {
    return schemaData.value
  }
  
  const searchLower = searchFilter.value.toLowerCase()
  return schemaData.value.filter(row => {
    if (row.type === 'competence') {
      return row.competence_index.toLowerCase().includes(searchLower) ||
             row.competence_name.toLowerCase().includes(searchLower) ||
             (row.competence_type && row.competence_type.toLowerCase().includes(searchLower))
    } else if (row.type === 'discipline') {
      return row.discipline_index.toLowerCase().includes(searchLower) ||
             row.discipline_name.toLowerCase().includes(searchLower)
    }
    return true
  })
})

const visibleRows = computed(() => {
  return filteredRows.value
})

const competenceCount = computed(() => {
  return schemaData.value.filter(row => row.type === 'competence').length
})

const disciplineCount = computed(() => {
  return schemaData.value.filter(row => row.type === 'discipline').length
})

// Методы
function getSemesterChipColor(value) {
  if (!value) return 'grey'
  
  // Цвета для разных типов данных в семестрах
  value = value.toLowerCase()
  if (value.includes('з') || value.includes('зач')) return 'blue'    // зачет
  if (value.includes('эк') || value.includes('экз')) return 'red'    // экзамен
  if (value.includes('кр') || value.includes('курс')) return 'orange' // курсовая работа
  if (value.includes('пр') || value.includes('практ')) return 'green'  // практика
  if (value.includes('кп') || value.includes('кр пр')) return 'purple' // курсовой проект
  
  return 'primary'
}

async function loadCompetenceSchema() {
  loading.value = true
  
  try {
    if (!store.currentPlanId) {
      throw new Error('План не выбран')
    }
    
    // 1. Загружаем матрицу компетенций
    const matrixResponse = await store.fetchCompetenceMatrix(store.currentPlanId)
    
    // 2. Загружаем все компетенции плана
    const competencesResponse = await store.fetchAllCompetences(store.currentPlanId)
    
    // 3. Загружаем все дисциплины плана
    await store.fetchAllDisciplines(store.currentPlanId)
    
    // 4. Формируем данные для схемы
    const competences = competencesResponse.competences || []
    const matrix = matrixResponse.matrix || []
    
    const schemaRows = []
    
    // Сортируем компетенции по типу и индексу
    const sortedCompetences = [...competences].sort((a, b) => {
      const typeA = getCompetenceType(a.competence_index)
      const typeB = getCompetenceType(b.competence_index)
      
      const typeOrder = {
        'Универсальная': 1,
        'Общепрофессиональная': 2,
        'Профессиональная': 3,
        'Дополнительная': 4,
        'Другая': 5
      }
      
      if (typeOrder[typeA] !== typeOrder[typeB]) {
        return typeOrder[typeA] - typeOrder[typeB]
      }
      
      return a.competence_index.localeCompare(b.competence_index)
    })
    
    // Проходим по всем компетенциям
    sortedCompetences.forEach(competence => {
      // Находим дисциплины, которые формируют эту компетенцию
      const disciplineRows = matrix
        .filter(item => item.type === 'discipline' && item.competence_indices_list)
        .filter(item => item.competence_indices_list.includes(competence.competence_index))
        .map(item => {
          return {
            id: `discipline_${item.index}_${competence.competence_index}`,
            type: 'discipline',
            discipline_index: item.index,
            discipline_name: item.name,
            parent_competence: competence.competence_index,
            semester_1: ' ',
            semester_2: ' ',
            semester_3: ' ',
            semester_4: ' ',
            semester_5: ' ',
            semester_6: ' ',
            semester_7: ' ',
            semester_8: ' '
          }
        })
      
      if (disciplineRows.length > 0) {
        // Добавляем строку компетенции
        schemaRows.push({
          id: `competence_${competence.competence_index}`,
          type: 'competence',
          competence_index: competence.competence_index,
          competence_name: competence.competence,
          competence_type: getCompetenceType(competence.competence_index)
        })
        
        // Добавляем дисциплины под компетенцией
        schemaRows.push(...disciplineRows)
      }
    })
    
    const competencesWithDisciplines = new Set(
      matrix
        .filter(item => item.type === 'discipline' && item.competence_indices_list)
        .flatMap(item => item.competence_indices_list)
    )
    
    const competencesWithoutDisciplines = competences.filter(
      comp => !competencesWithDisciplines.has(comp.competence_index)
    )
    
    if (competencesWithoutDisciplines.length > 0) {
      schemaRows.push({
        id: 'divider_no_disciplines',
        type: 'divider',
        label: `Компетенции без дисциплин (${competencesWithoutDisciplines.length})`
      })
      
      competencesWithoutDisciplines.forEach(competence => {
        schemaRows.push({
          id: `competence_no_disc_${competence.competence_index}`,
          type: 'competence',
          competence_index: competence.competence_index,
          competence_name: competence.competence,
          competence_type: getCompetenceType(competence.competence_index),
          warning: true
        })
      })
    }
    
    schemaData.value = schemaRows
    
  } catch (error) {
    console.error('Error loading competence schema:', error)
    $q.notify({
      type: 'negative',
      message: `Ошибка загрузки схемы компетенций: ${error.message}`,
      position: 'top-right'
    })
  } finally {
    loading.value = false
  }
}

function getCompetenceType(competenceIndex) {
  if (!competenceIndex) return 'Неизвестно'
  
  if (competenceIndex.includes('УК') || competenceIndex.startsWith('УК')) {
    return 'Универсальная'
  } else if (competenceIndex.includes('ОПК') || competenceIndex.startsWith('ОПК')) {
    return 'Общепрофессиональная'
  } else if (competenceIndex.includes('ПК') || competenceIndex.startsWith('ПК')) {
    return 'Профессиональная'
  } else if (competenceIndex.includes('ДК') || competenceIndex.startsWith('ДК')) {
    return 'Дополнительная'
  } else {
    return 'Другая'
  }
}

// Хуки жизненного цикла
watch(() => store.currentPlanId, (newPlanId) => {
  if (newPlanId) {
    loadCompetenceSchema()
  }
})

onMounted(() => {
  if (store.currentPlanId) {
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
    }
    
    // Семестры
    &.semester-1,
    &.semester-2 {
      background-color: rgba(232, 245, 233, 0.1) !important;
    }
    
    &.semester-3,
    &.semester-4 {
      background-color: rgba(227, 242, 253, 0.1) !important;
    }
    
    &.semester-5,
    &.semester-6 {
      background-color: rgba(255, 243, 224, 0.1) !important;
    }
    
    &.semester-7,
    &.semester-8 {
      background-color: rgba(252, 228, 236, 0.1) !important;
    }
  }
  
  // Строка компетенции
  .competence-row {
    td {
      padding: 12px !important;
    }
    
    .text-h6 {
      font-size: 1.1rem;
      font-weight: 600;
    }
  }
  
  // Строка дисциплины
  .discipline-row {
    transition: background-color 0.2s;
    
    &:hover {
      background-color: #f5f5f5 !important;
    }
  }
  
  // Разделитель
  .divider-row {
    td {
      padding: 8px !important;
    }
  }
  
  .bg-grey-1 {
    background-color: #fafafa !important;
  }
}

.q-chip {
  min-height: 20px;
  font-size: 10px;
  padding: 0 6px;
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
    
    td.text-truncate {
      max-width: 250px;
    }
  }
}
</style>