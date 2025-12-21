<template>
  <div class="text-h5 q-mb-sm">{{ sectionTitle }}</div>  
  <div class="text-subtitle1 text-grey">Раскройте для заполнения </div>

    <div v-if="error" class="q-pa-md">
      <q-banner dense class="bg-negative text-white">
        {{ error }}
        <template v-slot:action>
          <q-btn flat label="Повторить" @click="loadIndicators" />
        </template>
      </q-banner>
    </div>
    
    <div v-else>
      <div v-if="!competence" class="text-body1 text-grey text-center q-py-xl">
        <div>Выберите компетенцию для просмотра индикаторов</div>
      </div>

      <div v-else>
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
                    <div class="text-subtitle3 text-grey">Дисциплина: {{ indicator.discipline_index }} {{ indicator.discipline_name }}</div>
                  </div>
                  <div class="indicators-form row justify-between q-gutter-md">
                    <q-input
                      filled
                      label="Критерии оценивания"
                      stack-label
                      type="textarea"
                      class="col"
                      v-model="indicator.criteria"
                      bg-color="grey-4"
                      :readonly="indicator.saving"
                      debounce="1000"
                      @update:model-value="saveIndicator(indicator)"
                    />
                    <q-input
                      filled
                      label="Средства (методы) оценивания промежуточной аттестации"
                      stack-label
                      type="textarea"
                      class="col"
                      v-model="indicator.methods"
                      bg-color="grey-4"
                      :readonly="indicator.saving"
                      debounce="1000"
                      @update:model-value="saveIndicator(indicator)"
                    />
                  </div>
                </div>
              </q-expansion-item>
            </div>
          </q-list>
        </div>
        

        <div v-else class="text-body1 text-grey text-center q-py-xl">
          <div>Для данной компетенции нет индикаторов в конкретных дисциплинах</div>
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

const emit = defineEmits(['data-saved'])

const $q = useQuasar()
const store = useCompetencePassportStore()
const {
  competenceIndicatorsCreteria,
  loading
} = storeToRefs(store)

const sectionTitle = '3. Критерии и средства (методы) оценивания индикаторов достижения  компетенции в рамках промежуточной аттестации'

const error = ref(null)

const indicators = computed(() => {
  return competenceIndicatorsCreteria.value
})

const hasCompetenceData = computed(() => {
  return props.competence && props.competence.competence_index
})

async function loadIndicators() {
  if (!props.planId || !hasCompetenceData.value) {
    return
  }
  
  loading.value = true
  error.value = null
  
  try {
    await store.fetchCompetenceIndicators(props.planId, props.competence.competence_index)
  } catch (err) {
    error.value = err.response?.data?.error || 'Ошибка при загрузке индикаторов компетенции'
  } finally {
    loading.value = false
  }
}

async function saveIndicator(indicator) {
  if (!indicator.id) return

  indicator.saving = true
  indicator.saved = false
  
  try {
    await store.saveIndicatorDetails(indicator)
    
    indicator.saved = true
    $q.notify({
      message: 'Данные индикатора успешно обновлены',
      color: 'positive',
      position: 'bottom-right',
      timeout: 2000,
      html: true
    })
    
    emit('data-saved', indicator)
    setTimeout(() => {
      indicator.saved = false
    }, 3000)
    
  } catch (err) {
    $q.notify({
      message: 'Данные индикатора не сохранены',
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