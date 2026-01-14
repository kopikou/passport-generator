<template>
  <div class="q-mb-lg">
    <div class="text-h6 q-mb-md">{{ sectionTitle }}</div>
    <div class="text-grey q-mb-sm flex items-center justify-between">
      <span>Управление индикаторами достижения компетенций</span>
      <q-btn
        label="Добавить индикатор"
        icon="mdi-plus"
        color="primary"
        @click="addIndicator"
        :disabled="!competence || loading"
        class="q-ml-md"
      />
    </div>

    <div v-if="!competence" class="text-body1 text-grey text-center q-py-xl">
      <div>Выберите компетенцию для просмотра индикаторов</div>
    </div>

    <div v-else>
      <div v-if="indicators.length > 0" class="indicators-container">
        <div class="indicators-container__header text-center text-subtitle1 items-center bg-grey-2">
          <div class="cell-num">№</div>
          <div class="cell-code">Код индикатора</div>
          <div class="cell-content">Содержание индикатора</div>
          <div class="cell-disciplines">Дисциплины</div>
          <div class="cell-actions">Управление</div>
        </div>

        <div class="indicators-container__body" ref="indicatorsList">
          <div v-for="(indicator, index) in indicators" 
               :key="indicator.id"
               class="indicators-container__body__cell text-subtitle1"
               :class="getRowColor(index)"
               :data-id="indicator.id">
            <!-- Режим редактирования -->
            <div v-if="indicator.editingRow" class="editing-row">
              <div class="cell-num text-center">{{ index + 1 }}</div>
              <div class="cell-code text-center">
                <q-input
                  v-model="indicator.editingIndicatorIndex"
                  dense
                  outlined
                  @keyup.enter="saveRow(indicator)"
                />
              </div>
              <div class="cell-content">
                <q-input
                  v-model="indicator.editingContentText"
                  type="textarea"
                  autogrow
                  dense
                  outlined
                  @keyup.enter="saveRow(indicator)"
                />
              </div>
              <div class="cell-disciplines">
                <q-select
                  v-model="indicator.editingDisciplineId"
                  :options="availableDisciplines"
                  option-label="name"
                  option-value="id"
                  map-options
                  emit-value
                  dense
                  outlined
                  @keyup.enter="saveRow(indicator)"
                />
              </div>
              <div class="cell-actions text-center">
                <q-btn
                  icon="mdi-check"
                  color="green"
                  flat
                  dense
                  @click="saveRow(indicator)"
                  :loading="indicator.saving"
                  title="Сохранить"
                />
                <q-btn
                  icon="mdi-close"
                  color="red"
                  flat
                  dense
                  @click="cancelEditRow(indicator)"
                  :disabled="indicator.saving"
                  title="Отмена"
                />
              </div>
            </div>

            <div v-else class="viewing-row">
              <div class="cell-num text-center">{{ index + 1 }}</div>
              <div class="cell-code text-center">
                {{ indicator.indicator_index }}
              </div>
              <div class="cell-content text-justify">
                {{ indicator.indicator_content || 'Нет содержания' }}
              </div>
              <div class="cell-disciplines">
                <div v-if="indicator.discipline_index && indicator.discipline_name">
                  {{ indicator.discipline_index }} {{ indicator.discipline_name }}
                </div>
                <div v-else class="text-grey">
                  Не привязано
                </div>
              </div>
              <div class="cell-actions text-center">
                <q-btn
                  icon="mdi-pencil-outline"
                  color="green"
                  flat
                  dense
                  @click="editRow(indicator)"
                  :disabled="indicator.saving"
                  title="Редактировать строку"
                />
                <q-btn
                  icon="mdi-delete"
                  color="red"
                  flat
                  dense
                  @click="deleteIndicator(indicator)"
                  :disabled="indicator.saving"
                  title="Удалить"
                />
                <q-btn
                  v-if="index > 0"
                  icon="mdi-arrow-up-thin"
                  color="black"
                  flat
                  dense
                  @click="moveIndicatorUp(indicator)"
                  :disabled="indicator.saving"
                  title="Переместить вверх"
                />
                <q-btn
                  v-if="index < indicators.length - 1"
                  icon="mdi-arrow-down-thin"
                  color="black"
                  flat
                  dense
                  @click="moveIndicatorDown(indicator)"
                  :disabled="indicator.saving"
                  title="Переместить вниз"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="indicators.length === 0 && !loading" class="text-body1 text-grey text-center q-py-xl">
        <div>Для данной компетенции нет индикаторов</div>
      </div>

      <!-- Диалог добавления нового индикатора -->
      <q-dialog v-model="showAddDialog" persistent>
        <q-card style="min-width: 500px">
          <q-card-section>
            <div class="text-h6">Добавить новый индикатор</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-form @submit="createNewIndicator">
              <div class="q-gutter-md">
                <!-- Выбор дисциплины -->
                <q-select
                  v-model="newIndicator.discipline_id"
                  :options="availableDisciplines"
                  option-label="name"
                  option-value="id"
                  map-options
                  emit-value
                  label="Дисциплина"
                  filled
                  clearable
                  :rules="[val => !!val || 'Выберите дисциплину']"
                >
                  <template v-slot:option="scope">
                    <q-item v-bind="scope.itemProps">
                      <q-item-section>
                        <q-item-label>{{ scope.opt.name }}</q-item-label>
                        <q-item-label caption>{{ scope.opt.index }}</q-item-label>
                      </q-item-section>
                    </q-item>
                  </template>
                </q-select>

                <!-- Код индикатора -->
                <q-input
                  v-model="newIndicator.indicator_index"
                  label="Код индикатора"
                  filled
                  :rules="[val => !!val || 'Введите код индикатора']"
                />

                <!-- Содержание индикатора -->
                <q-input
                  v-model="newIndicator.indicator_content"
                  label="Содержание индикатора"
                  type="textarea"
                  filled
                  :rules="[val => !!val && val.length >= 10 || 'Введите содержание индикатора']"
                  autogrow
                />
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Отмена" color="negative" @click="cancelAddDialog" />
            <q-btn flat label="Сохранить" color="primary" @click="createNewIndicator" :loading="loading" />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, nextTick } from 'vue'
import { useQuasar } from 'quasar'
import { useCompetencePassportStore } from 'stores/competencePassportStore'
import { storeToRefs } from 'pinia'
import _ from 'lodash'

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

const $q = useQuasar()
const store = useCompetencePassportStore()
const {
  loading,
  currentPlanDisciplines
} = storeToRefs(store)

const sectionTitle = '2.1 Соотнесение индикаторов достижения компетенций с дисциплинами (модулями), практиками'

const error = ref(null)
const indicators = ref([])
const showAddDialog = ref(false)

const newIndicator = ref({
  discipline_id: null,
  indicator_index: '',
  indicator_content: ''
})

// Доступные дисциплины для выбора
const availableDisciplines = computed(() => {
  return (currentPlanDisciplines.value || []).map(discipline => ({
    id: discipline.id,
    name: discipline.dis,
    index: discipline.newdisid
  })).filter(disc => disc.index)
})

function getRowColor(index) {
  return index % 2 === 0 ? 'bg-grey-4' : 'bg-white'
}

async function loadIndicators() {
  if (!props.planId || !props.competence?.competence_index) {
    indicators.value = []
    return
  }
  
  try {
    const data = await store.fetchCompetenceIndicatorDisciplines(
      props.planId, 
      props.competence.competence_index
    )
    
    indicators.value = (data.table_data || []).map(item => ({
      ...item,
      editingRow: false,
      editingIndicatorIndex: item.indicator_index,
      editingContentText: item.indicator_content,
      editingDisciplineId: item.discipline_id,
      saving: false,
      saved: false
    }))
  } catch (err) {
    error.value = err.response?.data?.error || 'Ошибка при загрузке индикаторов'
    indicators.value = []
    $q.notify({
      message: 'Ошибка загрузки индикаторов',
      color: 'negative',
      position: 'bottom-right'
    })
  }
}

// Режим редактирования
function editRow(indicator) {
  indicators.value.forEach(item => {
    if (item.id !== indicator.id) {
      item.editingRow = false
    }
  })

  indicator.editingRow = true
  indicator.editingIndicatorIndex = indicator.indicator_index
  indicator.editingContentText = indicator.indicator_content
  indicator.editingDisciplineId = indicator.discipline_id

  nextTick(() => {
    const input = document.querySelector(`[data-id="${indicator.id}"] .cell-code input`)
    if (input) {
      input.focus()
    }
  })
}

function cancelEditRow(indicator) {
  indicator.editingRow = false
  indicator.editingIndicatorIndex = indicator.indicator_index
  indicator.editingContentText = indicator.indicator_content
  indicator.editingDisciplineId = indicator.discipline_id
}

async function saveRow(indicator) {
  if (!indicator.id) {
    indicator.editingRow = false
    return
  }
  
  indicator.saving = true
  
  try {
    const updateData = {
      indicator_id: indicator.id
    }

    if (indicator.editingIndicatorIndex !== indicator.indicator_index) {
      updateData.indicator_index = indicator.editingIndicatorIndex.trim()
    }
    
    if (indicator.editingContentText !== indicator.indicator_content) {
      updateData.indicator_content = indicator.editingContentText.trim()
    }
    
    if (indicator.editingDisciplineId !== indicator.discipline_id) {
      updateData.discipline_id = indicator.editingDisciplineId
    }

    if (Object.keys(updateData).length === 1) {
      indicator.editingRow = false
      indicator.saving = false
      return
    }
    
    const result = await store.updateIndicator(updateData)
    
    if (result.success) {
      Object.assign(indicator, {
        indicator_index: result.indicator.indicator_index,
        indicator_content: result.indicator.indicator_content,
        discipline_id: result.indicator.discipline_id,
        discipline_name: result.indicator.discipline_name,
        discipline_index: result.indicator.discipline_index,
        editingRow: false,
        saved: true
      })

      if (updateData.indicator_index) {
        await loadIndicators()
      } else {
        indicators.value = [...indicators.value]
      }

      $q.notify({
        message: 'Индикатор успешно обновлен',
        color: 'positive',
        position: 'bottom-right',
        timeout: 2000
      })

      setTimeout(() => {
        indicator.saved = false
      }, 3000)
    }
  } catch (err) {
    console.error('Ошибка при сохранении индикатора:', err)
    $q.notify({
      message: 'Ошибка при сохранении индикатора',
      color: 'negative',
      position: 'bottom-right'
    })
  } finally {
    indicator.saving = false
  }
}

// Перемещение индикаторов
async function moveIndicatorUp(indicator) {
  const index = indicators.value.findIndex(i => i.id === indicator.id)
  if (index <= 0) return
  
  try {
    [indicators.value[index - 1], indicators.value[index]] = 
    [indicators.value[index], indicators.value[index - 1]]

    $q.notify({
      message: 'Индикатор перемещен вверх',
      color: 'info',
      position: 'bottom-right',
      timeout: 1000
    })
  } catch (err) {
    console.error('Ошибка при перемещении индикатора:', err)
  }
}

async function moveIndicatorDown(indicator) {
  const index = indicators.value.findIndex(i => i.id === indicator.id)
  if (index >= indicators.value.length - 1) return
  
  try {
    [indicators.value[index], indicators.value[index + 1]] = 
    [indicators.value[index + 1], indicators.value[index]]

    $q.notify({
      message: 'Индикатор перемещен вниз',
      color: 'info',
      position: 'bottom-right',
      timeout: 1000
    })
  } catch (err) {
    console.error('Ошибка при перемещении индикатора:', err)
  }
}

function addIndicator() {
  newIndicator.value = {
    discipline_id: null,
    indicator_index: props.competence.competence_index ? `${props.competence.competence_index}.` : '',
    indicator_content: ''
  }
  showAddDialog.value = true
}

function cancelAddDialog() {
  showAddDialog.value = false
  newIndicator.value = {
    discipline_id: null,
    indicator_index: '',
    indicator_content: ''
  }
}

async function createNewIndicator() {
  if (!newIndicator.value.discipline_id || !newIndicator.value.indicator_index || 
      !newIndicator.value.indicator_content || newIndicator.value.indicator_content.length < 10) {
    $q.notify({
      message: 'Заполните все обязательные поля',
      color: 'warning',
      position: 'bottom-right'
    })
    return
  }

  try {
    const result = await store.createIndicator({
      plan_id: props.planId,
      discipline_id: newIndicator.value.discipline_id,
      competence_index: props.competence.competence_index,
      indicator_index: newIndicator.value.indicator_index,
      indicator_content: newIndicator.value.indicator_content,
      competence: props.competence.competence
    })
    
    if (result.success) {
      $q.notify({
        message: 'Индикатор успешно создан',
        color: 'positive',
        position: 'bottom-right'
      })
      
      indicators.value.unshift({
        ...result.indicator,
        editingRow: false,
        editingIndicatorIndex: result.indicator.indicator_index,
        editingContentText: result.indicator.indicator_content,
        editingDisciplineId: result.indicator.discipline_id,
        saving: false,
        saved: false
      })
      
      showAddDialog.value = false
      newIndicator.value = {
        discipline_id: null,
        indicator_index: '',
        indicator_content: ''
      }
    }
  } catch (err) {
    console.error('Ошибка при создании индикатора:', err)
    $q.notify({
      message: err.response?.data?.error || 'Ошибка при создании индикатора',
      color: 'negative',
      position: 'bottom-right'
    })
  }
}

async function deleteIndicator(indicator) {
  $q.dialog({
    title: 'Удаление индикатора',
    message: 'Вы точно хотите удалить индикатор?',
    ok: {
      label: 'Удалить',
      flat: true,
      color: 'red',
    },
    cancel: {
      label: 'Отмена',
      flat: true,
      color: 'green',
    },
    persistent: true
  }).onOk(async () => {
    try {
      const result = await store.deleteIndicator(indicator.id)
      
      if (result.success) {
        indicators.value = indicators.value.filter(i => i.id !== indicator.id)
        
        $q.notify({
          message: 'Индикатор успешно удален',
          color: 'positive',
          position: 'bottom-right'
        })
      }
    } catch (err) {
      console.error('Ошибка при удалении индикатора:', err)
      $q.notify({
        message: err.response?.data?.error || 'Ошибка при удалении индикатора',
        color: 'negative',
        position: 'bottom-right'
      })
    }
  })
}

async function loadDisciplines() {
  if (props.planId) {
    await store.fetchAllDisciplines(props.planId)
  }
}

watch(() => props.competence, (newCompetence) => {
  if (newCompetence && newCompetence.competence_index) {
    loadIndicators()
  }
}, { immediate: true })

watch(() => props.planId, (newPlanId) => {
  if (newPlanId) {
    loadDisciplines()
    if (props.competence?.competence_index) {
      loadIndicators()
    }
  }
})

onMounted(() => {
  if (props.planId) {
    loadDisciplines()
    if (props.competence?.competence_index) {
      loadIndicators()
    }
  }
})
</script>

<style scoped lang="scss">
.indicators-container {
  $border: solid 1px silver;

  &__header {
    display: grid;
    grid-template-columns: 50px 150px 1fr 250px 150px;
    grid-gap: 10px;
    font-weight: bold;
    border: $border;
    border-bottom: none;
    padding: 12px 8px;
    align-items: center;

    .cell-num,
    .cell-code,
    .cell-content,
    .cell-disciplines,
    .cell-actions {
      text-align: center;
    }
  }

  &__body {
    .indicators-container__body__cell {
      border: $border;
      border-bottom: none;

      &:last-child {
        border-bottom: $border;
      }

      .editing-row {
        display: grid;
        grid-template-columns: 50px 150px 1fr 250px 150px;
        grid-gap: 10px;
        padding: 12px 8px;
        align-items: center;

        .cell-num {
          text-align: center;
        }

        .cell-code {
          .q-input {
            width: 100%;
          }
        }

        .cell-content {
          .q-input {
            width: 100%;
          }
        }

        .cell-disciplines {
          .q-select {
            width: 100%;
          }
        }

        .cell-actions {
          text-align: center;
          display: flex;
          justify-content: center;
          gap: 5px;
          
          .q-btn {
            margin: 0 2px;
          }
        }
      }

      .viewing-row {
        display: grid;
        grid-template-columns: 50px 150px 1fr 250px 150px;
        grid-gap: 10px;
        padding: 12px 8px;
        min-height: 60px;
        align-items: center;

        .cell-content {
          word-break: break-word;
        }

        .cell-actions {
          display: flex;
          justify-content: center;
          gap: 5px;
          
          .q-btn {
            margin: 0 2px;
          }
        }
      }
    }
  }
}
</style>