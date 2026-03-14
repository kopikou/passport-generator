<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useQuasar } from 'quasar'
import { useCompetencePassportStore } from 'src/stores/competencePassportStore'
import { storeToRefs } from 'pinia'

const $q = useQuasar()
const store = useCompetencePassportStore()

const {
  passport,
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
    required: true
  }
})

const sectionTitle = '2. Индикаторы достижения компетенции'
//const finalIndicatorText = ref('')

const currentCompetence = computed(() => {
  if (!props.competence?.competence_index) return null
  
  const comp = passport.value.find(
    c => c.competence_index === props.competence.competence_index
  )

  return comp || null
})

async function saveData() {
  if (!currentCompetence.value) return

  try {
    await store.updateCompetenceFinalIndicators(
      props.planId,
      currentCompetence.value.competence_index,
      currentCompetence.value.competence_final_indicator//finalIndicatorText.value || ''
    )
    
    $q.notify({
      message: 'Данные итогового индикатора успешно обновлены',
      color: 'positive',
      position: 'top-right',
      timeout: 2000
    })
  } catch (error: any) {
    $q.notify({
      message: 'Ошибка сохранения итогового индикатора',
      color: 'negative',
      position: 'top-right',
      timeout: 3000
    })
  }
}

</script>

<template>
  <div class="competence-indicators-section">
    <div class="text-h6 q-mb-xs">{{ sectionTitle }}</div>
    <div class="text-grey q-mb-sm">
      Итоговый индикатор достижения компетенции. Данные автоматически получены из учебного плана
    </div>

    <div class="q-gutter-y-md">
      <q-input
        v-model="currentCompetence.competence_final_indicator"
        filled
        label="Итоговый индикатор достижения компетенции"
        type="textarea"
        stack-label
        rows="10"
        bg-color="grey-4"
        :loading="loading"
        :disable="saving"
        debounce="1000"
        @update:model-value="saveData"
      />
    </div>
  </div>
</template>

<style scoped lang="scss">

</style>