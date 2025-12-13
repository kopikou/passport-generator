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
        <component
          :is="currentSectionComponent"
          :plan-data="planData"
          :competence="currentCompetence"
          :plan-id="store.currentPlanId"
          @data-saved="handleDataSaved"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, defineAsyncComponent } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCompetencePassportStore } from 'stores/competencePassportStore'
import { useQuasar } from 'quasar'

const route = useRoute()
const router = useRouter()
const store = useCompetencePassportStore()
const $q = useQuasar()

const loading = ref(false)
const currentCompetence = ref(null)
const planData = ref(null)

// импорты компонентов
const sectionComponents = {
  'title-page': defineAsyncComponent(() => 
    import('./components/menu_sections/TitlePageSection.vue')
  ),
  'competence-relations': defineAsyncComponent(() => 
    import('./components/menu_sections/CompetenceRelationsSection.vue')
  ),
  'competence-indicators': defineAsyncComponent(() => 
    import('./components/menu_sections/CompetenceIndicatorsSection.vue')
  ),
  'indicator-disciplines': defineAsyncComponent(() => 
    import('./components/menu_sections/IndicatorDisciplinesSection.vue')
  ),
  'indicator-results': defineAsyncComponent(() => 
    import('./components/menu_sections/IndicatorResultsSection.vue')
  ),
  'assessment-criteria': defineAsyncComponent(() => 
    import('./components/menu_sections/AssessmentCriteriaSection.vue')
  )
}

const selectedSection = computed(() => {
  return route.query.section
})

const pageTitle = computed(() => {
  return route.meta.title || 'Паспорт компетенций'
})

const currentSectionComponent = computed(() => {
  return sectionComponents[selectedSection.value]
})

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

const handleDataSaved = (message) => {
  $q.notify({
    message: message,
    color: "secondary",
    position: "bottom-right",
    html: true,
  })
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
  }
}
</style>