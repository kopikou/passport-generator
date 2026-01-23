<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useQuasar } from 'quasar'
import { useCompetencePassportStore } from 'src/stores/competencePassportStore'
import { storeToRefs } from 'pinia'

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
    required: true
  }
})

const $q = useQuasar()
const store = useCompetencePassportStore()

const {
  passport,
  disciplines,
  loading,
  saving
} = storeToRefs(store)

const sectionTitle = '2.1 Соотнесение индикаторов достижения компетенций с дисциплинами (модулями), практиками'
const showAddDialog = ref(false)
const showEditDialog = ref(false)
const editingIndicator = ref<any>(null)
const newIndicator = ref({
  discipline_id: null,
  indicator_index: '',
  indicator_content: ''
})

const currentIndicators = computed(() => {
  if (!props.competence?.competence_index) return []
  
  const comp = passport.value.find(
    c => c.competence_index === props.competence.competence_index
  )
  
  return comp?.indicator_list || []
})

const availableDisciplines = computed(() => {
  return disciplines.value.map(discipline => ({
    id: discipline.discipline_id,
    name: discipline.discipline_name,
    index: discipline.discipline_index
  })).filter(d => d.index)
})

function getRowColor(index){
  return index % 2 === 0 ? 'bg-grey-4' : 'bg-white'
}

function startEdit(indicator) {
  editingIndicator.value = {
    ...indicator,
    original_indicator_index: indicator.indicator_index,
    original_indicator: indicator.indicator,
    original_discipline_id: indicator.discipline_id
  }
  showEditDialog.value = true
}

async function saveEdit() {
  if (!editingIndicator.value) return
  
  try {
    const updateData: any = {
      indicator_id: editingIndicator.value.indicator_id
    }
    
    // Обновление индекса
    if (editingIndicator.value.indicator_index !== editingIndicator.value.original_indicator_index) {
      updateData.indicator_index = editingIndicator.value.indicator_index.trim()
    }
    
    // Обновление содержания
    if (editingIndicator.value.indicator !== editingIndicator.value.original_indicator) {
      updateData.indicator = editingIndicator.value.indicator.trim()
    }
    
    // Обновление дисциплины
    if (editingIndicator.value.discipline_id !== editingIndicator.value.original_discipline_id) {
      updateData.discipline_id = editingIndicator.value.discipline_id
    }
    
    if (Object.keys(updateData).length > 1) {
      await store.updateIndicator(
        editingIndicator.value.indicator_id,
        updateData
      )
      
      $q.notify({
        message: 'Индикатор успешно обновлен',
        color: 'positive',
        position: 'top-right',
        timeout: 2000
      })
    }
    
    showEditDialog.value = false
    editingIndicator.value = null
    
  } catch (error: any) {
    $q.notify({
      message: 'Ошибка при сохранении индикатора',
      color: 'negative',
      position: 'top-right'
    })
  }
}

async function createNewIndicator() {
  if (!newIndicator.value.discipline_id || 
      !newIndicator.value.indicator_index || 
      !newIndicator.value.indicator_content) {
    $q.notify({
      message: 'Заполните все обязательные поля',
      color: 'warning',
      position: 'top-right'
    })
    return
  }

  try {
    await store.createIndicator({
      //plan_id: props.planId,
      discipline_id: newIndicator.value.discipline_id,
      competence_index: props.competence.competence_index,
      competence: props.competence.competence,
      indicator_index: newIndicator.value.indicator_index,
      indicator: newIndicator.value.indicator_content
    })
    
    $q.notify({
      message: 'Индикатор успешно создан',
      color: 'positive',
      position: 'top-right'
    })
    
    showAddDialog.value = false
    newIndicator.value = {
      discipline_id: null,
      indicator_index: '',
      indicator_content: ''
    }
  } catch (error: any) {
    $q.notify({
      message: 'Ошибка при создании индикатора',
      color: 'negative',
      position: 'top-right'
    })
  }
}

function addIndicator() {
  newIndicator.value = {
    discipline_id: null,
    indicator_index: props.competence?.competence_index ? `${props.competence.competence_index}.` : '',
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

function cancelEditDialog() {
  showEditDialog.value = false
  editingIndicator.value = null
}

async function deleteIndicator(indicatorId) {
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
      await store.deleteIndicator(indicatorId)
      
      $q.notify({
        message: 'Индикатор успешно удален',
        color: 'positive',
        position: 'top-right'
      })
    } catch (error: any) {
      $q.notify({
        message: 'Ошибка при удалении индикатора',
        color: 'negative',
        position: 'top-right'
      })
    }
  })
}

// Перемещение индикаторов с обменом индексов
async function moveIndicatorUp(indicator) {
  const currentIndex = currentIndicators.value.findIndex(i => i.indicator_id === indicator.indicator_id)
  if (currentIndex <= 0) return
  
  try {
    const targetIndex = currentIndex - 1
    const targetIndicator = currentIndicators.value[targetIndex]
    
    const currentOriginalIndex = indicator.indicator_index
    const targetOriginalIndex = targetIndicator.indicator_index
    
    await Promise.all([
      store.updateIndicator(indicator.indicator_id, { indicator_index: targetOriginalIndex }),
      store.updateIndicator(targetIndicator.indicator_id, { indicator_index: currentOriginalIndex })
    ])
    
    $q.notify({
      message: 'Индикаторы успешно перемещены',
      color: 'positive',
      position: 'top-right',
      timeout: 1500
    })
    
  } catch (error: any) {
    $q.notify({
      message: 'Ошибка при перемещении индикатора',
      color: 'negative',
      position: 'top-right'
    })
  }
}

async function moveIndicatorDown(indicator) {
  const currentIndex = currentIndicators.value.findIndex(i => i.indicator_id === indicator.indicator_id)
  if (currentIndex >= currentIndicators.value.length - 1) return
  
  try {
    const targetIndex = currentIndex + 1
    const targetIndicator = currentIndicators.value[targetIndex]
    
    const currentOriginalIndex = indicator.indicator_index
    const targetOriginalIndex = targetIndicator.indicator_index
    
    await Promise.all([
      store.updateIndicator(indicator.indicator_id, { indicator_index: targetOriginalIndex }),
      store.updateIndicator(targetIndicator.indicator_id, { indicator_index: currentOriginalIndex })
    ])
    
    $q.notify({
      message: 'Индикаторы успешно перемещены',
      color: 'positive',
      position: 'top-right',
      timeout: 1500
    })
    
  } catch (error: any) {
    $q.notify({
      message: 'Ошибка при перемещении индикатора',
      color: 'negative',
      position: 'top-right'
    })
  }
}
</script>

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
      <div v-if="currentIndicators.length > 0" class="indicators-container">
        <div class="indicators-container__header text-center text-subtitle1 items-center bg-grey-2">
          <div class="cell-num">№</div>
          <div class="cell-code">Код индикатора</div>
          <div class="cell-content">Содержание индикатора</div>
          <div class="cell-disciplines">Дисциплины</div>
          <div class="cell-actions">Управление</div>
        </div>

        <div class="indicators-container__body">
          <div 
            v-for="(indicator, index) in currentIndicators" 
            :key="indicator.id"
            class="indicators-container__body__cell text-subtitle1"
            :class="getRowColor(index)"
          >
            <div class="viewing-row">
              <div class="cell-num text-center">{{ index + 1 }}</div>
              <div class="cell-code text-center">
                {{ indicator.indicator_index }}
              </div>
              <div class="cell-content text-justify">
                {{ indicator.indicator || 'Нет содержания' }}
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
                  @click="startEdit(indicator)"
                  :disabled="saving"
                  title="Редактировать строку"
                />
                <q-btn
                  icon="mdi-delete"
                  color="red"
                  flat
                  dense
                  @click="deleteIndicator(indicator.indicator_id)"
                  :disabled="saving"
                  title="Удалить"
                />
                <q-btn
                  v-if="index > 0"
                  icon="mdi-arrow-up-thin"
                  color="black"
                  flat
                  dense
                  @click="moveIndicatorUp(indicator)"
                  :disabled="saving"
                  title="Переместить вверх"
                />
                <q-btn
                  v-if="index < currentIndicators.length - 1"
                  icon="mdi-arrow-down-thin"
                  color="black"
                  flat
                  dense
                  @click="moveIndicatorDown(indicator)"
                  :disabled="saving"
                  title="Переместить вниз"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="currentIndicators.length === 0 && !loading" class="text-body1 text-grey text-center q-py-xl">
        <div>Для данной компетенции нет индикаторов</div>
      </div>

      <!-- Диалог добавления нового индикатора -->
      <q-dialog v-model="showAddDialog" persistent>
        <q-card style="min-width: 500px">
          <q-card-section>
            <div class="text-h6">Добавить новый индикатор</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-form @submit.prevent="createNewIndicator">
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
                  :rules="[val => !!val || 'Введите содержание индикатора']"
                  autogrow
                />
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Отмена" color="negative" @click="cancelAddDialog" />
            <q-btn flat label="Сохранить" color="primary" @click="createNewIndicator" :loading="saving" />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <!-- Диалог редактирования индикатора -->
      <q-dialog v-model="showEditDialog" persistent>
        <q-card style="min-width: 500px">
          <q-card-section>
            <div class="text-h6">Редактировать индикатор</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-form @submit.prevent="saveEdit">
              <div class="q-gutter-md">
                <!-- Код индикатора -->
                <q-input
                  v-model="editingIndicator.indicator_index"
                  label="Код индикатора"
                  filled
                  :rules="[val => !!val || 'Введите код индикатора']"
                />

                <!-- Содержание индикатора -->
                <q-input
                  v-model="editingIndicator.indicator"
                  label="Содержание индикатора"
                  type="textarea"
                  filled
                  :rules="[val => !!val || 'Введите содержание индикатора']"
                  autogrow
                />

                <!-- Выбор дисциплины -->
                <q-select
                  v-model="editingIndicator.discipline_id"
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
              </div>
            </q-form>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="Отмена" color="negative" @click="cancelEditDialog" />
            <q-btn flat label="Сохранить" color="primary" @click="saveEdit" :loading="saving" />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </div>
</template>

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