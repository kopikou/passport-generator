<script setup lang="ts">
import { ref, computed} from 'vue'
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
  saving
} = storeToRefs(store)

const sectionTitle = '2.2 Соотнесение индикаторов достижения компетенций с результатами обучения по дисциплинам (модулям), практикам'

const currentIndicators = computed(() => {
  if (!props.competence?.competence_index) return []
  
  const comp = passport.value.find(
    c => c.competence_index === props.competence.competence_index
  )
  
  return comp?.indicator_list || []
})

async function saveIndicator(indicator) {
  if (!indicator.indicator_id) return
  
  try {
    await store.updateIndicatorDetails({
      indicator_id: indicator.indicator_id,
      know: indicator.know,
      able: indicator.able,
      own: indicator.own,
      criteria: indicator.criteria,
      methods: indicator.methods
    })
    
    $q.notify({
      message: 'Данные индикатора успешно обновлены',
      color: 'positive',
      position: 'top-right',
      timeout: 2000
    })
    
  } catch (error: any) {
    $q.notify({
      message: 'Ошибка при сохранении данных индикатора',
      color: 'negative',
      position: 'top-right',
      timeout: 3000
    })
  }
}
</script>

<template>
  <div class="q-mb-lg q-pb-lg">
    <div class="text-h6">{{ sectionTitle }}</div>  
    <div class="text-grey q-mb-sm">Раскройте для заполнения</div>

    <div v-if="!competence" class="text-body1 text-grey text-center q-py-xl">
      <div>Выберите компетенцию для просмотра индикаторов</div>
    </div>

    <div v-else>
      <!-- Список индикаторов -->
      <div v-if="currentIndicators.length > 0">
        <q-list bordered>
          <div v-for="(indicator, index) in currentIndicators" :key="indicator.indicator_index">
            <q-expansion-item
              :label="`${indicator.indicator_index} ${indicator.indicator || ''}`"
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
                    label="Знать"
                    stack-label
                    type="textarea"
                    class="col"
                    v-model="indicator.know"
                    bg-color="grey-4"
                    :disable="saving"
                    debounce="1000"
                    @update:model-value="() => saveIndicator(indicator)"
                  />
                  <q-input
                    filled
                    label="Уметь"
                    stack-label
                    type="textarea"
                    class="col"
                    v-model="indicator.able"
                    bg-color="grey-4"
                    :disable="saving"
                    debounce="1000"
                    @update:model-value="() => saveIndicator(indicator)"
                  />
                  <q-input
                    filled
                    label="Владеть"
                    stack-label
                    type="textarea"
                    class="col"
                    v-model="indicator.own"
                    bg-color="grey-4"
                    :disable="saving"
                    debounce="1000"
                    @update:model-value="() => saveIndicator(indicator)"
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

<style scoped lang="scss">
.indicators-form {
  > .col {
    flex-basis: 400px;
  }
}
</style>