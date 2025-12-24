<template>
  <div class="text-h6">{{ sectionTitle }}</div>
  <div class="text-grey q-mb-sm">Итоговый индикатор достижения компетенции.  Данные автоматически получены из учебного плана</div>

  <div class="q-gutter-y-md">
    <q-input
      v-model="finalIndicatorText"
      filled
      label="Итоговый индикатор достижения компетенции"
      type="textarea"
      stack-label
      rows="10"
      bg-color="grey-4"
      :readonly="disabled"
      :loading="loading"
      debounce="1000"
      @update:model-value="saveData"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useQuasar } from 'quasar'
import { useCompetencePassportStore } from 'stores/competencePassportStore'
import { storeToRefs } from 'pinia'

const $q = useQuasar()
const store = useCompetencePassportStore()
const {
  saving,
  loading
} = storeToRefs(store)

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

const sectionTitle = '2. Индикаторы достижения компетенции'
const finalIndicatorText = ref('')
const disabled = ref(false)

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
    await store.updateCompetenceFinalIndicators(
      props.planId,
      props.competence.competence_index,
      finalIndicatorText.value || ''
    )

    $q.notify({
      message: 'Данные итогового индикатора успешно обновлены',
      color: 'positive',
      position: 'bottom-right',
      timeout: 2000,
      html: true
    })
  } catch (error) {
    console.error('Ошибка сохранения итогового индикатора:', error)
    $q.notify({
      message: 'Ошибка сохранения итогового индикатора',
      color: 'negative',
      position: 'bottom-right',
      timeout: 3000,
      html: true
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

</style>