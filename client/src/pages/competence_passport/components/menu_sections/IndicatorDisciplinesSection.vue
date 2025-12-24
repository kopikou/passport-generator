<template>
  <div class="q-mb-lg">
    <div class="text-h6">{{ sectionTitle }}</div>  
    <div class="text-grey q-mb-sm">Индикаторы и их содержание автоматически получены из учебного плана</div>

    <div v-if="!competence" class="text-body1 text-grey text-center q-py-xl">
      <div>Выберите компетенцию для просмотра индикаторов</div>
    </div>

    <div v-else>
      <!-- Список индикаторов -->
      <div v-if="indicators.length > 0">
        <q-list bordered>
          <div v-for="(indicator, index) in indicators" :key="indicator.id">
            <q-expansion-item
              :label="`${indicator.indicator_index} ${indicator.indicator_content || ''}`"
              :default-opened="index === 0"
              group="indicators"
            >
              <div class="q-pa-sm">
                <div class="q-mb-md">
                  <div class="text-subtitle3 text-grey">
                    Дисциплина: {{ indicator.discipline_index }} {{ indicator.discipline_name }}
                  </div>
                </div>
                
                <div class="indicators-form row justify-between q-gutter-md">
                  <q-input
                    filled
                    label="Содержание индикатора"
                    stack-label
                    type="textarea"
                    class="col"
                    v-model="indicator.editingContent"
                    bg-color="grey-4"
                    :readonly="indicator.saving"
                    debounce="1000"
                    @update:model-value="saveIndicatorContent(indicator)"
                  />
                </div>
              </div>
            </q-expansion-item>
          </div>
        </q-list>
      </div>

      <div v-else class="text-body1 text-grey text-center q-py-xl">
        <div v-if="loading">Загрузка...</div>
        <div v-else>Для данной компетенции нет индикаторов в конкретных дисциплинах</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useCompetencePassportStore } from 'stores/competencePassportStore'
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
    default: ''
  }
})

const $q = useQuasar()
const store = useCompetencePassportStore()
const {
  loading
} = storeToRefs(store)

const sectionTitle = '2.1. Соотнесение индикаторов с дисциплинами'

const error = ref(null)
const indicators = ref([])

const hasCompetenceData = computed(() => {
  return props.competence && props.competence.competence_index
})

async function loadIndicators() {
  if (!props.planId || !hasCompetenceData.value) {
    indicators.value = []
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    const data = await store.fetchCompetenceIndicatorDisciplines(
      props.planId, 
      props.competence.competence_index
    )

    indicators.value = (data.table_data || []).map(item => ({
      ...item,
      editingContent: item.indicator_content,
      saving: false,
      saved: false
    }))
  } catch (err) {
    error.value = err.response?.data?.error || 'Ошибка при загрузке индикаторов с дисциплинами'
    indicators.value = []
    $q.notify({
      message: 'Ошибка загрузки индикаторов с дисциплинами',
      color: 'negative',
      position: 'bottom-right'
    })
  } finally {
    loading.value = false
  }
}

async function saveIndicatorContent(indicator) {
  if (!indicator.id || !indicator.editingContent || 
      indicator.editingContent.trim() === indicator.indicator_content) {
    return
  }
  
  indicator.saving = true
  indicator.saved = false
  
  try {
    const result = await store.updateIndicatorContent(indicator.id, indicator.editingContent.trim())
    
    if (result.success) {
      indicator.indicator_content = result.indicator.indicator_content
      indicator.is_final = result.indicator.is_final
      indicator.saved = true

      $q.notify({
        message: 'Содержание индикатора успешно обновлено',
        color: 'positive',
        position: 'bottom-right',
        timeout: 2000,
        html: true
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
      position: 'bottom-right',
      timeout: 3000,
      html: true
    })
  } finally {
    indicator.saving = false
  }
}

watch(() => props.competence, (newCompetence) => {
  if (newCompetence && newCompetence.competence_index) {
    loadIndicators()
  }
}, { immediate: true })

watch(() => props.planId, (newPlanId) => {
  if (newPlanId && hasCompetenceData.value) {
    loadIndicators()
  }
})

onMounted(() => {
  if (props.planId && hasCompetenceData.value) {
    loadIndicators()
  }
})
</script>

<style scoped lang="scss">
.indicators-form {
  > .col {
    flex-basis: 400px;
  }
}
</style>