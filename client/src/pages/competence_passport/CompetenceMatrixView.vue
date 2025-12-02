<template>
  <top-navigation-menu>
    <template #content>
      <div class="q-pa-md">
        <div class="row items-center q-mb-md">
          <div class="col">
            <h2 class="text-h4 q-ma-none">Матрица компетенций</h2>
            <div class="text-subtitle1 text-grey">
              Соответствие дисциплины и формируемых компетенций
            </div>
          </div>
          <div class="col-auto">
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
            <q-input
              v-model="searchFilter"
              placeholder="Поиск по дисциплинам, группам или индексам..."
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
          :rows="visibleMatrix"
          :columns="columns"
          row-key="index"
          :loading="matrixLoading"
          :pagination="pagination"
          binary-state-sort
          flat
          bordered
          virtual-scroll
          style="height: calc(100vh - 200px);"
        >
          <template v-slot:top>
            <div class="text-h6">Показано строк: {{ visibleMatrix.length }} из {{ store.competenceMatrix.length }}</div>
            <q-space />
            <div class="text-caption text-grey" v-if="searchFilter">
              Поиск: "{{ searchFilter }}"
            </div>
          </template>

          <template v-slot:body="props">
            <q-tr 
              :props="props" 
              :class="{ 'clickable-row': props.row.type === 'discipline' }"
              @dblclick="onRowDoubleClick(props.row)"
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
                    :icon="isExpanded(props.row.index) ? 'remove' : 'add'"
                    @click.stop="toggleGroup(props.row.index)"
                    class="q-mr-xs"
                    style="min-width: 24px; min-height: 24px;"
                  />
                  <q-icon 
                    v-else-if="props.row.type === 'group'" 
                    :name="getGroupIcon(props.row.level)" 
                    class="q-mr-xs"
                    size="16px"
                  />
                  <span style="width: 16px; display: inline-block;" v-else></span>
                  {{ props.row.index }}
                </div>
              </q-td>
              
              <q-td key="name" :props="props">
                <div 
                  :class="[
                    props.row.type === 'group' ? 'text-bold' : '',
                    `level-${props.row.level}`
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
                  Нет компетенций
                </div>
              </q-td>
            </q-tr>
          </template>
        </q-table>
        
        <!-- Модальное окно редактирования -->
        <discipline-competences-editor
          v-if="editingRow"
          :plan-id="store.currentPlanId"
          :discipline-id="editingRow.id"
          :discipline-index="editingRow.index"
          :discipline-name="editingRow.name"
          :show="showEditor"
          @update:show="showEditor = $event"
          @saved="onCompetencesSaved"
        />
        <div v-if="debugInfo" class="q-pa-sm bg-yellow-2 text-caption">
          Отладка: editingRow = {{ editingRow }}, showEditor = {{ showEditor }}
        </div>
      </div>
    </template>
  </top-navigation-menu>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useCompetencePassportStore } from 'stores/competencePassportStore'
import TopNavigationMenu from './components/TopNavigationMenu.vue'
import DisciplineCompetencesEditor from './components/DisciplineCompetencesEditor.vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const store = useCompetencePassportStore()
const matrixLoading = ref(false)
const searchFilter = ref('')
const currentPlan = ref(null)
const expandedGroups = ref(new Set())
const pagination = ref({
  sortBy: 'index',
  descending: false,
  page: 1,
  rowsPerPage: 0
})

// Новые переменные для редактирования
const showEditor = ref(false)
const editingRow = ref(null)
const disciplinesMap = ref({}) // Кэш дисциплин для быстрого поиска
const debugInfo = ref(true) // Включите для отладки

const columns = [
  {
    name: 'index',
    required: true,
    label: 'Индекс',
    align: 'left',
    field: row => row.index,
    sortable: true,
    style: 'width: 150px;'
  },
  {
    name: 'name',
    required: true,
    label: 'Наименование',
    align: 'left',
    field: row => row.name,
    sortable: true,
    style: 'width: 350px;'
  },
  {
    name: 'competence_indices',
    label: 'Формируемые компетенции',
    align: 'left',
    field: row => row.competence_indices,
    sortable: false,
    style: 'min-width: 400px;'
  }
]

// Функция для определения цвета по типу компетенции
function getCompetenceBadgeColor(competenceIndex) {
  if (!competenceIndex) return 'grey'
  
  if (competenceIndex.includes('УК') || competenceIndex.startsWith('УК')) return 'blue'
  if (competenceIndex.includes('ОПК') || competenceIndex.startsWith('ОПК')) return 'green'
  if (competenceIndex.includes('ПК') || competenceIndex.startsWith('ПК')) return 'orange'
  if (competenceIndex.includes('ДК') || competenceIndex.startsWith('ДК')) return 'purple'
  
  return 'grey'
}

// Функция для получения иконки группы по уровню
function getGroupIcon(level) {
  const icons = [
    'folder',      // уровень 1
    'folder_open', // уровень 2
    'folder',      // уровень 3
    'folder_open', // уровень 4
    'folder'       // уровень 5
  ]
  return icons[level - 1] || 'folder'
}

function hasChildren(groupIndex) {
  const allItems = store.competenceMatrix
  return allItems.some(item => 
    item.index !== groupIndex && 
    item.index.startsWith(groupIndex + '.')
  )
}

function isExpanded(groupIndex) {
  return expandedGroups.value.has(groupIndex)
}

// Переключаем состояние группы (раскрыть/скрыть)
function toggleGroup(groupIndex) {
  if (expandedGroups.value.has(groupIndex)) {
    expandedGroups.value.delete(groupIndex)
  } else {
    expandedGroups.value.add(groupIndex)
  }
}

// Раскрыть все группы
function expandAll() {
  const allItems = store.competenceMatrix
  allItems.forEach(item => {
    if (item.type === 'group' && hasChildren(item.index)) {
      expandedGroups.value.add(item.index)
    }
  })
}

// Свернуть все группы
function collapseAll() {
  expandedGroups.value.clear()
}

// Получаем все родительские группы для элемента
function getParentGroups(itemIndex) {
  const parents = []
  const parts = itemIndex.split('.')
  
  for (let i = 1; i < parts.length; i++) {
    const parentIndex = parts.slice(0, i).join('.')
    parents.push(parentIndex)
  }
  
  return parents
}

// Проверяем, виден ли элемент в текущем состоянии
function isItemVisible(item) {
  const parentGroups = getParentGroups(item.index)
  
  for (const parentIndex of parentGroups) {
    // Если родитель - группа и она не раскрыта, элемент не виден
    const parentItem = store.competenceMatrix.find(g => g.index === parentIndex && g.type === 'group')
    if (parentItem && !expandedGroups.value.has(parentIndex)) {
      return false
    }
  }
  
  return true
}

const filteredMatrix = computed(() => {
  let filtered = store.competenceMatrix
  
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

// Функция для загрузки дисциплин плана
async function loadDisciplines() {
  if (!store.currentPlanId) return
  
  try {
    await store.fetchAllDisciplines(store.currentPlanId)
    
    disciplinesMap.value = {}
    
    const disciplines = store.currentPlanDisciplines
    
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

// Обработчик двойного клика
async function onRowDoubleClick(row) {
  
  if (row.type !== 'discipline') {
    return
  }
  
  if (!store.currentPlanId) {
    $q.notify({
      type: 'warning',
      message: 'План не выбран. Пожалуйста, выберите учебный план.',
      position: 'top-right'
    })
    return
  }
  
  // Проверяем, загружены ли дисциплины
  const disciplines = store.currentPlanDisciplines
  
  if (!disciplines || disciplines.length === 0) {
    await loadDisciplines()
  }
  
  // Проверяем, создана ли карта дисциплин
  if (Object.keys(disciplinesMap.value).length === 0) {
    // Если нет, пробуем создать из текущих дисциплин
    disciplines.forEach(discipline => {
      if (discipline && discipline.newdisid) {
        disciplinesMap.value[discipline.newdisid] = discipline
      }
    })
  }
  
  // Ищем дисциплину в карте дисциплин
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
  
  loadCompetenceMatrix()
  loadDisciplines()
}

async function loadCompetenceMatrix() {
  matrixLoading.value = true
  try {
    const planId = store.currentPlanId
    
    if (!planId) {
      return
    }
    
    // Загружаем матрицу компетенций
    const response = await store.fetchCompetenceMatrix(planId)
    currentPlan.value = {
      planname: response.plan_name,
      abbrprofile: response.abbrprofile
    }
    
    const allItems = store.competenceMatrix
    allItems.forEach(item => {
      if (item.type === 'group' && item.level <= 2 && hasChildren(item.index)) {
        expandedGroups.value.add(item.index)
      }
    })
    
    await loadDisciplines()
    
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

watch(() => store.currentPlanId, (newPlanId) => {
  if (newPlanId) {
    disciplinesMap.value = {}
    loadCompetenceMatrix()
  }
})

onMounted(() => {
  if (store.currentPlanId) {
    loadCompetenceMatrix()
  }
})

</script>

<style scoped lang="scss">
.competence-indices-cell {
  max-height: 200px;
  overflow-y: auto;
  padding: 8px;
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

.expand-button {
  min-width: 24px;
  min-height: 24px;
  width: 24px;
  height: 24px;
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

:deep(.q-table) {
  .q-virtual-scroll {
    overflow: auto;
  }
  
  .q-badge {
    font-size: 12px;
    line-height: 1.2;
  }
  
  .q-td {
    padding: 8px 16px;
  }
}
</style>