<template>
  <div class="competence-relations-section">
    <div class="text-h5 q-mb-sm">{{ sectionTitle }}</div>
    <div class="section-details">
      <div class="text-subtitle1 text-grey">Для чего необходимо формирование компетенции</div>
      <div class="q-gutter-y-md">
        <q-input
          v-model="relationsText"
          filled
          type="textarea"
          placeholder="Связь компетенции с иными компетенциями"
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

const sectionTitle = '1.1. Связь компетенции с иными компетенциями'
const relationsText = ref('')
const disabled = ref(false)
const loading = ref(false)
const saving = ref(false)

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
    
    emit('data-saved', 'Связи компетенции успешно сохранены')
  } catch (error) {
    console.error('Ошибка сохранения связей компетенции:', error)
    $q.notify({
      message: 'Ошибка сохранения связей компетенции',
      color: 'negative',
      position: 'bottom-right'
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
.competence-relations-section {
  .section-details {
    margin-top: 16px;
    
    .text-subtitle1 {
      margin-bottom: 8px;
    }
    
    .q-card {
      min-height: 100px;
      margin-top: 8px;
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