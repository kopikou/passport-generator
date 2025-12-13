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
            debounce="1000"
            @update:model-value="saveData"
          />
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'

const $q = useQuasar()
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
    type: String,
    default: ''
  }
})

const emit = defineEmits(['data-saved'])

const sectionTitle = '1.1. Связь компетенции с иными компетенциями'
const relationsText = ref('')
const disabled = ref(false)
const loading = ref(false)

const loadData = async () => {
  if (!props.planId || !props.competence?.competence_index) {
    relationsText.value = ''
    return
  }

  loading.value = true
  try {
    const response = await api.get('/api/competence/competence-relations/', {
      params: {
        plan_id: props.planId,
        competence_index: props.competence.competence_index
      }
    })
    
    if (response.data && response.data.relations_text) {
      relationsText.value = response.data.relations_text
    } else {
      relationsText.value = ''
    }
  } catch (error) {
    relationsText.value = ''
  } finally {
    loading.value = false
  }
}

const saveData = async () => {
  if (!props.planId || !props.competence || !relationsText.value) {
    return
  }

  try {
    const response = await api.post('/api/competence/save-competence-relations/', {
      plan_id: props.planId,
      competence_index: props.competence.competence_index,
      relations_text: relationsText.value
    })
    
    if (response.status === 200) {
      emit('data-saved', "Данные <span class='text-bold'>о связи компетенции</span> сохранены!")
    }
  } catch (error) {
    console.error('Ошибка сохранения данных связи компетенции:', error)
    emit('data-saved', "Данные <span class='text-bold'>о связи компетенции</span> не сохранены!")
  }
}

onMounted(() => {
  loadData()
})

watch(() => props.competence, () => {
  loadData()
}, { immediate: true })
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
    }
  }
}
</style>