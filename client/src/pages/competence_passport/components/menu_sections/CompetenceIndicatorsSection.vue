<template>
  <div class="competence-indicators-section">
    <div class="text-h5 q-mb-sm">{{ sectionTitle }}</div>
    <div class="section-details">
      <div class="text-subtitle1 text-grey">Итоговый индикатор достижения компетенции.  Данные автоматически получены из учебного плана.</div>
      <div class="q-gutter-y-md">
        <q-input
          v-model="finalIndicatorText"
          filled
          type="textarea"
          placeholder="Итоговый индикатор достижения компетенции"
          rows="10"
          bg-color="grey-4"
          :readonly="disabled"
          :loading="loading"
          debounce="1000"
          @update:model-value="saveData"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
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

const sectionTitle = '2. Индикаторы достижения компетенции'
const finalIndicatorText = ref('')
const disabled = ref(false)
const loading = ref(false)
const saving = ref(false)

const loadIndicators = async () => {
  if (!props.planId || !props.competence?.competence_index) {
    finalIndicatorText.value = ''
    return
  }

  loading.value = true
  try {
    const data = await store.fetchCompetenceFinalIndicators(
      props.planId, 
      props.competence.competence_index
    )
    
    if (data.primary_indicator?.indicator) {
      finalIndicatorText.value = data.primary_indicator.indicator
    } else {
      finalIndicatorText.value = ''
    }
  } catch (error) {
    console.error('Ошибка загрузки индикаторов компетенции:', error)
    finalIndicatorText.value = ''
    $q.notify({
      message: 'Ошибка загрузки индикаторов компетенции',
      color: 'negative',
      position: 'bottom-right'
    })
  } finally {
    loading.value = false
  }
}

const saveData = async () => {
  if (!props.planId || !props.competence?.competence_index || saving.value) {
    return
  }

  saving.value = true
  try {
    const result = await store.updateCompetenceFinalIndicators(
      props.planId,
      props.competence.competence_index,
      finalIndicatorText.value || ''
    )
    
    if (result.success) {
      emit('data-saved', result.message || 'Итоговый индикатор успешно сохранен')
    }
  } catch (error) {
    console.error('Ошибка сохранения итогового индикатора:', error)
    $q.notify({
      message: 'Ошибка сохранения итогового индикатора',
      color: 'negative',
      position: 'bottom-right'
    })
  } finally {
    saving.value = false
  }
}

watch(() => props.competence, (newCompetence) => {
  if (newCompetence) {
    loadIndicators()
  }
}, { immediate: true })

watch(() => props.planId, (newPlanId) => {
  if (newPlanId && props.competence) {
    loadIndicators()
  }
})

onMounted(() => {
  if (props.planId && props.competence) {
    loadIndicators()
  }
})
</script>

<style scoped lang="scss">
.competence-indicators-section {
  .section-details {
    margin-top: 16px;
    
    .text-subtitle1 {
      margin-bottom: 8px;
    }
    
    .q-input {
      .q-field__control {
        background: #f5f5f5;
      }
      
      &.q-field--loading {
        .q-field__control:after {
          background: rgba(255, 255, 255, 0.7);
        }
      }
    }
  }
}
</style>