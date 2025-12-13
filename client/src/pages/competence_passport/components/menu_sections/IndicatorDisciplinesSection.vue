<template>
  <div class="indicator-disciplines-section">
    <div class="text-h5 q-mb-sm">{{ sectionTitle }}</div>
    <div class="section-details">
      <div class="text-subtitle1 text-grey">
        Индикаторы и их содержание автоматически получены из учебного плана.
      </div>

      <div class="q-mt-md">
        <q-table
          :rows="tableData"
          :columns="columns"
          row-key="id"
          :loading="loading"
          :pagination="pagination"
          flat
          bordered
          :no-data-label="noDataMessage"
          class="competence-table"
          :style="{ 'table-layout': 'fixed', 'width': '100%' }"
        >

          <template v-slot:top>
            <div class="text-h6">
              Всего индикаторов: {{ tableData.length }}
            </div>
          </template>

          <template v-slot:body-cell-indicator_index="props">
            <q-td :props="props" class="indicator-index-cell">
              <div class="text-weight-bold text-primary">
                {{ props.value }}
              </div>
            </q-td>
          </template>

          <template v-slot:body-cell-indicator_content="props">
            <q-td :props="props" class="indicator-content-cell">
              <div v-if="!props.row.editing" class="indicator-text" @dblclick="startEditing(props.row)">
                {{ props.value }}
                <q-icon 
                  name="edit" 
                  size="xs" 
                  class="q-ml-xs edit-icon"
                  @click="startEditing(props.row)"
                />
              </div>
              <div v-else class="edit-container">
                <q-input
                  v-model="props.row.editingContent"
                  type="textarea"
                  autogrow
                  dense
                  outlined
                  class="edit-input"
                  @keyup.enter="saveIndicatorContent(props.row)"
                  @keyup.esc="cancelEditing(props.row)"
                />
                <div class="edit-actions q-mt-sm">
                  <q-btn 
                    size="sm" 
                    color="primary" 
                    @click="saveIndicatorContent(props.row)"
                    :loading="saving"
                  >
                    Сохранить
                  </q-btn>
                  <q-btn 
                    size="sm" 
                    flat 
                    color="grey" 
                    @click="cancelEditing(props.row)"
                    class="q-ml-sm"
                  >
                    Отмена
                  </q-btn>
                </div>
              </div>
            </q-td>
          </template>

          <template v-slot:body-cell-discipline="props">
            <q-td :props="props" class="discipline-cell">
              <div class="discipline-text">
                {{ props.value }}
              </div>
            </q-td>
          </template>
        </q-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useQuasar } from 'quasar'
import { useCompetencePassportStore } from 'stores/competencePassportStore'

const $q = useQuasar()
const store = useCompetencePassportStore()

const props = defineProps({
  planData: {
    type: Object,
    default: () => ({})
  },
  competence: {
    type: Object,
    default: null
  },
  planId: {
    type: Number,
    default: ''
  }
})

const emit = defineEmits(['data-saved'])

const sectionTitle = '2.1. Соотнесение индикаторов с дисциплинами'
const tableData = ref([])
const loading = ref(false)
const saving = ref(false)
const finalIndicatorsCount = ref(0)

const editingRowId = ref(null)

const columns = [
  {
    name: 'indicator_index',
    required: true,
    label: 'Код',
    align: 'left',
    field: row => row.indicator_index,
    style: 'width: 100px !important; min-width: 100px !important; max-width: 100px !important;'
  },
  {
    name: 'indicator_content',
    required: true,
    label: 'Содержание индикатора',
    align: 'left',
    field: row => row.editing ? row.editingContent : row.indicator_content,
    style: 'width: 800px !important; min-width: 800px !important; max-width: 800px !important;'
  },
  {
    name: 'discipline',
    required: true,
    label: 'Дисциплины',
    align: 'left',
    field: row => row.discipline_name,
    style: 'width: 300px !important; min-width: 300px !important; max-width: 300px !important;'
  }
]

const pagination = {
  sortBy: 'indicator_index',
  descending: false,
  page: 1,
  rowsPerPage: 0
}

const noDataMessage = computed(() => {
  if (loading.value) return 'Загрузка...'
  if (!props.competence) return 'Выберите компетенцию'
  if (tableData.value.length === 0) return 'Для этой компетенции нет индикаторов'
  return 'Нет данных'
})

const startEditing = (row) => {
  if (editingRowId.value && editingRowId.value !== row.id) {
    const previousRow = tableData.value.find(r => r.id === editingRowId.value)
    if (previousRow) {
      cancelEditing(previousRow)
    }
  }
  
  row.editing = true
  row.editingContent = row.indicator_content
  editingRowId.value = row.id
}

const cancelEditing = (row) => {
  row.editing = false
  delete row.editingContent
  if (editingRowId.value === row.id) {
    editingRowId.value = null
  }
}

const saveIndicatorContent = async (row) => {
  if (!row.editingContent || row.editingContent.trim() === row.indicator_content) {
    cancelEditing(row)
    return
  }
  
  saving.value = true
  try {
    const result = await store.updateIndicatorContent(row.id, row.editingContent.trim())
    
    if (result.success) {
      row.indicator_content = result.indicator.indicator_content
      row.is_final = result.indicator.is_final
      
      $q.notify({
        message: 'Содержание индикатора успешно обновлено',
        color: 'positive',
        position: 'bottom-right'
      })
      
      emit('data-saved', {
        indicatorId: row.id,
        newContent: row.indicator_content
      })
    }
  } catch (error) {
    console.error('Ошибка при сохранении индикатора:', error)
    $q.notify({
      message: 'Ошибка при сохранении индикатора',
      color: 'negative',
      position: 'bottom-right'
    })
  } finally {
    saving.value = false
    cancelEditing(row)
  }
}

const loadData = async () => {
  if (!props.planId || !props.competence?.competence_index) {
    tableData.value = []
    finalIndicatorsCount.value = 0
    return
  }

  loading.value = true
  try {
    const data = await store.fetchCompetenceIndicatorDisciplines(
      props.planId, 
      props.competence.competence_index
    )

    tableData.value = (data.table_data || []).map(item => ({
      ...item,
      editing: false
    }))
    finalIndicatorsCount.value = data.final_indicators_count || 0
  } catch (error) {
    console.error('Ошибка загрузки индикаторов с дисциплинами:', error)
    tableData.value = []
    finalIndicatorsCount.value = 0
    $q.notify({
      message: 'Ошибка загрузки индикаторов с дисциплинами',
      color: 'negative',
      position: 'bottom-right'
    })
  } finally {
    loading.value = false
  }
}

watch(() => props.competence, (newCompetence) => {
  if (newCompetence) {
    loadData()
  }
}, { immediate: true })

watch(() => props.planId, (newPlanId) => {
  if (newPlanId && props.competence) {
    loadData()
  }
})

onMounted(() => {
  if (props.planId && props.competence) {
    loadData()
  }
})
</script>

<style scoped lang="scss">
.indicator-disciplines-section {
  .section-details {
    margin-top: 16px;
    
    .text-subtitle1 {
      margin-bottom: 8px;
    }
    
    .competence-table {
      margin-top: 1rem;
    }
  }
}

:deep(.competence-table) {
  table-layout: fixed !important;
  width: 100% !important;
  
  th:nth-child(1),
  td:nth-child(1) {
    width: 100px !important;
    min-width: 100px !important;
    max-width: 100px !important;
  }
  
  th:nth-child(2),
  td:nth-child(2) {
    width: 800px !important;
    min-width: 800px !important;
    max-width: 800px !important;
  }
  
  th:nth-child(3),
  td:nth-child(3) {
    width: 300px !important;
    min-width: 300px !important;
    max-width: 300px !important;
  }
}

:deep(.indicator-content-cell) {
  .indicator-text {
    word-wrap: break-word !important;
    white-space: normal !important;
    line-height: 1.4;
    cursor: pointer;
    padding: 4px 0;
    
    &:hover {
      background-color: #f5f5f5;
      border-radius: 4px;
      padding: 4px 8px;
    }
  }
  
  .edit-icon {
    opacity: 0.4;
    cursor: pointer;
    
    &:hover {
      opacity: 1;
      color: #1976d2;
    }
  }
  
  .edit-container {
    .edit-input {
      width: 100%;
    }
    
    .edit-actions {
      display: flex;
      justify-content: flex-start;
    }
  }
}

:deep(.discipline-cell) {
  .discipline-text {
    word-wrap: break-word !important;
    white-space: normal !important;
    line-height: 1.4;
  }
}

.text-weight-bold {
  font-weight: 600;
}

.text-primary {
  color: #1976d2;
}

:deep(.q-table) {
  table-layout: fixed;
}

:deep(.q-table th),
:deep(.q-table td) {
  vertical-align: top;
  padding: 12px 16px;
}

:deep(.q-table__card) {
  overflow-x: auto;
}
</style>