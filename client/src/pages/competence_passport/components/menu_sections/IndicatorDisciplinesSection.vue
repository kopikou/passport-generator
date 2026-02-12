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

const dialogMode = ref<'create' | 'edit' | null>(null)
const dialogIndicator = ref<any>(null)

const showDialog = computed({
  get: () => dialogMode.value !== null,
  set: (value) => {
    if (!value) {
      dialogMode.value = null
      dialogIndicator.value = null
    }
  }
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

const columns = [
  {
    name: 'number',
    label: '№',
    field: 'number',
    align: 'center',
    style: 'width: 50px'
  },
  {
    name: 'code',
    label: 'Код индикатора',
    field: 'indicator_index',
    align: 'center',
    style: 'width: 150px'
  },
  {
    name: 'content',
    label: 'Содержание индикатора',
    field: 'indicator',
    align: 'left',
    style: 'min-width: 300px'
  },
  {
    name: 'disciplines',
    label: 'Дисциплины',
    field: 'discipline',
    align: 'left',
    style: 'width: 250px'
  },
  {
    name: 'actions',
    label: 'Управление',
    field: 'actions',
    align: 'center',
    style: 'width: 150px'
  }
]

const tableRows = computed(() => {
  return currentIndicators.value.map((indicator, index) => ({
    ...indicator,
    number: index + 1,
    discipline: indicator.discipline_index && indicator.discipline_name 
      ? `${indicator.discipline_index} ${indicator.discipline_name}`
      : 'Не привязано'
  }))
})

const dialogContent = computed({
  get() {
    return dialogIndicator.value?.indicator_content || dialogIndicator.value?.indicator || ''
  },
  set(value) {
    if (dialogIndicator.value) {
      if (dialogMode.value === 'create') {
        dialogIndicator.value.indicator_content = value
      } else {
        dialogIndicator.value.indicator = value
      }
    }
  }
})

function openDialog(mode: 'create' | 'edit', indicator: any = null) {
  dialogMode.value = mode
  
  if (mode === 'create') {
    dialogIndicator.value = {
      discipline_id: null,
      indicator_index: props.competence?.competence_index ? `${props.competence.competence_index}.` : '',
      indicator_content: ''
    }
  } else {
    dialogIndicator.value = {
      ...indicator,
      original_indicator_index: indicator.indicator_index,
      original_indicator: indicator.indicator,
      original_discipline_id: indicator.discipline_id
    }
  }
}

async function saveDialog() {
  try {
    if (dialogMode.value === 'create') {
      if (!dialogIndicator.value.discipline_id || 
          !dialogIndicator.value.indicator_index || 
          !dialogIndicator.value.indicator_content) {
        $q.notify({
          message: 'Заполните все обязательные поля',
          color: 'warning',
          position: 'top-right'
        })
        return
      }

      await store.createIndicator({
        discipline_id: dialogIndicator.value.discipline_id,
        competence_index: props.competence.competence_index,
        competence: props.competence.competence,
        indicator_index: dialogIndicator.value.indicator_index,
        indicator: dialogIndicator.value.indicator_content
      })
      
      $q.notify({
        message: 'Индикатор успешно создан',
        color: 'positive',
        position: 'top-right'
      })
      
    } else {
      const updateData: any = {
        indicator_id: dialogIndicator.value.indicator_id
      }
      
      if (dialogIndicator.value.indicator_index !== dialogIndicator.value.original_indicator_index) {
        updateData.indicator_index = dialogIndicator.value.indicator_index.trim()
      }
      
      if (dialogIndicator.value.indicator !== dialogIndicator.value.original_indicator) {
        updateData.indicator = dialogIndicator.value.indicator.trim()
      }
      
      if (dialogIndicator.value.discipline_id !== dialogIndicator.value.original_discipline_id) {
        updateData.discipline_id = dialogIndicator.value.discipline_id
      }
      
      if (Object.keys(updateData).length > 1) {
        await store.updateIndicator(
          dialogIndicator.value.indicator_id,
          updateData
        )
        
        $q.notify({
          message: 'Индикатор успешно обновлен',
          color: 'positive',
          position: 'top-right',
          timeout: 2000
        })
      }
    }

    dialogMode.value = null
    dialogIndicator.value = null
    
  } catch (error: any) {
    $q.notify({
      message: dialogMode.value === 'create' 
        ? 'Ошибка при создании индикатора' 
        : 'Ошибка при сохранении индикатора',
      color: 'negative',
      position: 'top-right'
    })
  }
}

function addIndicator() {
  openDialog('create')
}

function startEdit(indicator) {
  openDialog('edit', indicator)
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
  <div class="q-mb-lg q-pb-lg">
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
      <q-table
        v-if="currentIndicators.length > 0"
        :rows="tableRows"
        :columns="columns"
        row-key="indicator_id"
        :loading="loading"
        :pagination="{ rowsPerPage: 0 }"
        flat
        bordered
        separator="cell"
        wrap-cells
        class="indicators-table"
      >
        <template v-slot:body-cell-disciplines="props">
          <q-td :props="props">
            <div :class="{ 'text-grey': !props.row.discipline_index }">
              {{ props.row.discipline }}
            </div>
          </q-td>
        </template>

        <template v-slot:body-cell-actions="props">
          <q-td :props="props" class="actions-cell">
            <div class="row q-gutter-xs justify-center">
              <q-btn
                icon="mdi-pencil-outline"
                color="green"
                flat
                dense
                size="sm"
                @click="startEdit(props.row)"
                :disabled="saving"
                title="Редактировать"
              />
              <q-btn
                icon="mdi-delete"
                color="red"
                flat
                dense
                size="sm"
                @click="deleteIndicator(props.row.indicator_id)"
                :disabled="saving"
                title="Удалить"
              />
              <q-btn
                v-if="props.row.number > 1"
                icon="mdi-arrow-up-thin"
                color="black"
                flat
                dense
                size="sm"
                @click="moveIndicatorUp(props.row)"
                :disabled="saving"
                title="Переместить вверх"
              />
              <q-btn
                v-if="props.row.number < currentIndicators.length"
                icon="mdi-arrow-down-thin"
                color="black"
                flat
                dense
                size="sm"
                @click="moveIndicatorDown(props.row)"
                :disabled="saving"
                title="Переместить вниз"
              />
            </div>
          </q-td>
        </template>
      </q-table>

      <div v-if="currentIndicators.length === 0 && !loading" class="text-body1 text-grey text-center q-py-xl">
        <div>Для данной компетенции нет индикаторов</div>
      </div>

      <q-dialog v-model="showDialog" persistent>
        <q-card style="min-width: 500px">
          <q-card-section>
            <div class="text-h6">
              {{ dialogMode === 'create' ? 'Добавить новый индикатор' : 'Редактировать индикатор' }}
            </div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-form @submit.prevent="saveDialog">
              <div class="q-gutter-md">
                <q-select
                  v-model="dialogIndicator.discipline_id"
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

                <q-input
                  v-model="dialogIndicator.indicator_index"
                  label="Код индикатора"
                  filled
                  :rules="[val => !!val || 'Введите код индикатора']"
                />

                <q-input
                  v-model="dialogContent"
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
            <q-btn flat label="Отмена" color="negative" @click="() => { dialogMode = null; dialogIndicator = null }" />
            <q-btn flat label="Сохранить" color="primary" @click="saveDialog" :loading="saving" />
          </q-card-actions>
        </q-card>
      </q-dialog>
    </div>
  </div>
</template>

<style scoped lang="scss">
.indicators-table {
  .q-table__middle {
    min-height: auto;
  }
  
  .actions-cell {
    padding: 8px !important;
    
    .q-btn {
      margin: 0 2px;
    }
  }
}
</style>