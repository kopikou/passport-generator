<template>
  <div class="competence-passport-view">
    <!-- Заголовок раздела -->
    <div class="section-header q-mb-md">
      <div class="text-h4 q-mb-xs">{{ pageTitle }}</div>
      <div v-if="currentCompetence" class="text-subtitle1 text-grey">
        {{ currentCompetence.competence_index }} - {{ currentCompetence.competence }}
      </div>
    </div>

    <!-- Основной контент -->
    <div v-if="!selectedSection" class="empty-state q-pa-xl text-center">
      <span
        style="align-content: center; text-align: center; font-size: 20px; font-weight: bold"
      >
        Выберите нужный раздел слева
      </span>
    </div>

    <div v-else class="passport-content">
      <!-- Динамический контент по разделам -->
      <div v-if="loading" class="text-center q-pa-lg">
        <q-spinner color="primary" size="2em" />
        <div class="text-caption q-mt-sm">Загрузка данных...</div>
      </div>

      <div v-else class="section-content">
        <!-- Титульный лист -->
        <div v-if="selectedSection === 'title-page'" class="title-page-section">
          <div class="text-h5 q-mb-sm">Титульный лист</div>
          <div class="q-gutter-y-sm">
            <div v-if="planData?.admission?.cadmkind != 5">
              <div class="text-subtitle1 q-mb-xs">Профиль/Специальность</div>
              <q-field outlined dense>
                <template v-slot:control>
                  <div class="self-center full-width no-outline">{{ planData?.admission?.spec_name }}</div>
                </template>
              </q-field>
            </div>
            
            <div v-if="planData?.admission?.cadmkind != 5">
              <div class="text-subtitle1 q-mb-xs">Наименование направления</div>
              <q-field outlined dense>
                <template v-slot:control>
                  <div class="self-center full-width no-outline">{{ planData?.admission?.direct_name }}</div>
                </template>
              </q-field>
            </div>
            
            <div v-if="planData?.admission?.cadmkind == 5">
              <div class="text-subtitle1 q-mb-xs">Наименование направления</div>
              <q-field outlined dense>
                <template v-slot:control>
                  <div class="self-center full-width no-outline">{{ getSpecName(planData?.admission?.spec_name) }}</div>
                </template>
              </q-field>
            </div>
            
            <div v-if="planData?.admission?.cadmkind == 5">
              <div class="text-subtitle1 q-mb-xs">Направленность</div>
              <q-field outlined dense>
                <template v-slot:control>
                  <div class="self-center full-width no-outline">{{ getSpecNapr(planData?.admission?.spec_name) }}</div>
                </template>
              </q-field>
            </div>
            
            <div>
              <div class="text-subtitle1 q-mb-xs">Факультет</div>
              <q-field outlined dense>
                <template v-slot:control>
                  <div class="self-center full-width no-outline">{{ planData?.admission?.cfac__name }}</div>
                </template>
              </q-field>
            </div>
          </div>
        </div>

        <template v-else>
          <div class="text-h5 q-mb-sm">{{ sectionTitle }}</div>
          <!-- Контент конкретного раздела -->
          <div class="section-details">
            <div v-if="selectedSection === 'competence-relations'">
              <div class="text-subtitle1 text-grey">Для чего необходимо формирование компетенции</div>
              <q-card flat bordered class="q-pa-md">
                <div class="text-body1 text-grey">
                  Раздел находится в разработке...
                </div>
              </q-card>
            </div>

            <div v-else-if="selectedSection === 'competence-indicators'">
              <div class="text-subtitle1 text-grey">Итоговый индикатор достижения компетенции.  Данные автоматически получены из учебного плана.</div>
              <q-card flat bordered class="q-pa-md">
                <div class="text-body1 text-grey">
                  Раздел находится в разработке...
                </div>
              </q-card>
            </div>

            <div v-else-if="selectedSection === 'indicator-disciplines'">
              <div class="text-subtitle1 text-grey">Индикаторы и их содержание автоматически получены из учебного плана.</div>
              <q-card flat bordered class="q-pa-md">
                <div class="text-body1 text-grey">
                  Раздел находится в разработке...
                </div>
              </q-card>
            </div>

            <div v-else-if="selectedSection === 'indicator-results'">
              <div class="text-subtitle1 text-grey">Раскройте для заполнения</div>
              <q-card flat bordered class="q-pa-md">
                <div class="text-body1 text-grey">
                  Раздел находится в разработке...
                </div>
              </q-card>
            </div>

            <div v-else-if="selectedSection === 'assessment-criteria'">
              <div class="text-subtitle1 text-grey">Раскройте для заполнения</div>
              <q-card flat bordered class="q-pa-md">
                <div class="text-body1 text-grey">
                  Раздел находится в разработке...
                </div>
              </q-card>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCompetencePassportStore } from 'stores/competencePassportStore'

const route = useRoute()
const router = useRouter()
const store = useCompetencePassportStore()

const loading = ref(false)
const currentCompetence = ref(null)
const planData = ref(null)

const selectedSection = computed(() => {
  return route.query.section
})

const pageTitle = computed(() => {
  return route.meta.title || 'Паспорт компетенций'
})

const sectionTitle = computed(() => {
  const sections = {
    'title-page': 'Титульный лист',
    'competence-relations': '1.1 Связь компетенции с иными компетенциями',
    'competence-indicators': '2 Индикаторы достижения компетенции',
    'indicator-disciplines': '2.1 Соотнесение индикаторов достижения компетенций с дисциплинами  (модулями), практиками',
    'indicator-results': '2.2 Соотнесение индикаторов достижения компетенций с результатами обучения  по дисциплинам (модулям), практикам',
    'assessment-criteria': '3 Критерии и средства (методы) оценивания индикаторов достижения  компетенции в рамках промежуточной аттестации'
  }
  return sections[selectedSection.value] || 'Паспорт компетенции'
})

const getCompetenceType = (competenceIndex) => {
  if (!competenceIndex) return 'Неизвестно'
  
  if (competenceIndex.includes('УК') || competenceIndex.startsWith('УК')) {
    return 'Универсальная'
  }
  if (competenceIndex.includes('ОПК') || competenceIndex.startsWith('ОПК')) {
    return 'Общепрофессиональная'
  }
  if (competenceIndex.includes('ПК') || competenceIndex.startsWith('ПК')) {
    return 'Профессиональная'
  }
  if (competenceIndex.includes('ДК') || competenceIndex.startsWith('ДК')) {
    return 'Дополнительная'
  }
  
  return 'Другая'
}

// Методы для титульного листа
const getSpecNapr = (name) => {
  if (!name) return 'Отсутствует'
  const names = name.split("направленность")
  if (names.length > 1) {
    return names[1].replace(' - ', '')
  } else {
    return 'Отсутствует'
  }
}

const getSpecName = (name) => {
  if (!name) return ''
  const names = name.split("направленность")
  if (names.length > 1) {
    return names[0].replace(', ', '')
  } else {
    return name
  }
}

// Загрузка данных плана для титульного листа
const loadPlanData = async () => {
  if (!store.currentPlanId) {
    planData.value = null
    return
  }

  loading.value = true
  try {
    const competencesData = await store.fetchAllCompetences(store.currentPlanId)
    
    if (competencesData) {
      planData.value = {
        plan_id: competencesData.plan_id,
        plan_mira_id: competencesData.plan_mira_id,
        plan_name: competencesData.plan_name,
        abbrprofile: competencesData.abbrprofile,
        admission: {
          cadmkind: 1, 
          spec_name: competencesData.plan_name,
          direct_name: competencesData.abbrprofile,
          cfac__name: 'Не указано'
        },
      }
      try {
        const planResponse = await store.fetchPlanDetails(store.currentPlanId)
        if (planResponse) {
          planData.value = {
            ...planData.value,
            ...planResponse
          }
        }
      } catch (error) {
        console.warn('Не удалось загрузить детальные данные плана:', error)
      }
    }
  } catch (error) {
    console.error('Ошибка загрузки данных плана:', error)
    planData.value = null
  } finally {
    loading.value = false
  }
}

const loadCompetenceData = async (competenceIndex) => {
  if (!competenceIndex || !store.currentPlanId) {
    currentCompetence.value = null
    return
  }

  loading.value = true
  try {
    const data = await store.fetchAllCompetences(store.currentPlanId)
    
    const competence = data?.competences?.find(
      comp => comp.competence_index === competenceIndex
    )
    
    if (competence) {
      currentCompetence.value = competence
    } else {
      currentCompetence.value = null
      console.warn(`Компетенция ${competenceIndex} не найдена в плане ${store.currentPlanId}`)
    }
  } catch (error) {
    console.error('Ошибка загрузки данных компетенции:', error)
    currentCompetence.value = null
  } finally {
    loading.value = false
  }
}

watch(
  () => route.query,
  (newQuery) => {
    if (newQuery.section === 'title-page') {
      loadPlanData()
      currentCompetence.value = null
    } else if (newQuery.competence) {
      loadCompetenceData(newQuery.competence)
    } else {
      currentCompetence.value = null
    }
  },
  { immediate: true, deep: true }
)

watch(
  () => store.currentPlanId,
  (newPlanId) => {
    if (newPlanId) {
      if (route.query.section === 'title-page') {
        loadPlanData()
      } else if (route.query.competence) {
        loadCompetenceData(route.query.competence)
      }
    } else {
      currentCompetence.value = null
      planData.value = null
    }
  }
)

onMounted(() => {
  if (route.query.section === 'title-page' && store.currentPlanId) {
    loadPlanData()
  } else if (route.query.competence && store.currentPlanId) {
    loadCompetenceData(route.query.competence)
  }
})


</script>

<style scoped lang="scss">
.competence-passport-view {
  min-height: 100%;
  
  .section-header {
    border-bottom: 1px solid #e0e0e0;
    padding-bottom: 16px;
    
    .text-subtitle1 {
      font-size: 16px;
      line-height: 1.4;
    }
  }
  
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 400px;
    
    span {
      font-size: 20px;
      font-weight: bold;
      line-height: 1.5;
    }
  }
  
  .passport-content {
    min-height: 300px;
  }
  
  .section-content {
    max-width: 1200px;
    margin: 0 auto;
    
    .text-h5 {
      margin-bottom: 8px;
    }
  }
  
  .title-page-section {
    .q-field {
      margin-bottom: 12px;
      
      &:last-child {
        margin-bottom: 0;
      }
      
      .q-field__control {
        background: #f5f5f5;
        min-height: 40px;
      }
    }
  }
  
  .section-details {
    margin-top: 16px;
    
    .text-subtitle1 {
      margin-bottom: 8px;
    }
    
    .q-card {
      min-height: 100px;
      margin-top: 8px;
    }
  }
}

.q-badge {
  font-size: 12px;
  padding: 4px 10px;
  font-weight: 500;
}
</style>