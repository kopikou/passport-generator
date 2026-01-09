<template>
  <div class="text-h6">{{ sectionTitle }}</div>
  <div class="text-grey q-mb-sm">Для чего необходимо формирование компетенции</div>

  <div class="q-gutter-y-md">
    <q-input
      v-model="relationsText"
      filled
      type="textarea"
      label="Связь компетенции с иными компетенциями"
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

const sectionTitle = '1.1. Связь компетенции с иными компетенциями'
const relationsText = ref('')
const disabled = ref(false)

const loadRelations = async () => {
  if (!props.planId || !props.competence?.competence_index) {
    relationsText.value = ''
    return
  }

  loading.value = true
  try {
    const data = await store.fetchCompetenceRelations(
      props.planId, 
      props.competence.competence_index
    )
    
    if (data.relations) {
      relationsText.value = data.relations
    } else {
      relationsText.value = ''
    }
  } catch (error) {
    console.error('Ошибка загрузки связей компетенции:', error)
    relationsText.value = ''
    $q.notify({
      message: 'Ошибка загрузки связей компетенции',
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
    await store.updateCompetenceRelations(
      props.planId,
      props.competence.competence_index,
      relationsText.value || ''
    )
    
    $q.notify({
      message: 'Связи компетенций успешно сохранены',
      color: 'positive',
      position: 'bottom-right',
      timeout: 2000,
      html: true
    })
  } catch (error) {
    console.error('Ошибка сохранения связей компетенции:', error)
    $q.notify({
      message: 'Ошибка сохранения связей компетенции',
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
    loadRelations()
  }
}, { immediate: true })

watch(() => props.planId, (newPlanId) => {
  if (newPlanId && props.competence) {
    loadRelations()
  }
})

onMounted(() => {
  if (props.planId && props.competence) {
    loadRelations()
  }
})
</script>

<style scoped lang="scss">

</style>