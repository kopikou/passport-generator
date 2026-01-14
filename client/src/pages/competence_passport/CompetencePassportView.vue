<template>
  <div class="competence-passport-view">
    <div class="section-header q-mb-md">
      <div class="text-h4 q-mb-xs">{{ pageTitle }}</div>
      <div v-if="currentCompetence" class="text-subtitle1 text-grey">
        {{ currentCompetence.competence_index }} - {{ currentCompetence.competence }}
      </div>
      <div v-else-if="selectedSection === 'title-page'" class="text-subtitle1 text-grey">
        Титульный лист паспорта компетенций
      </div>
    </div>

    <div v-if="!selectedSection" class="empty-state q-pa-xl text-center">
      <span style="align-content: center; text-align: center; font-size: 20px; font-weight: bold">
        Выберите нужный раздел слева
      </span>
    </div>

    <div v-else class="passport-content">
      <!-- Вкладки для разделов компетенции -->
      <div v-if="selectedSection && selectedSection !== 'title-page'" class="competence-tabs q-mb-lg">
        <q-tabs
          v-model="activeTab"
          align="left"
          class="q-mb-md"
          active-bg-color="teal-1"
          @update:model-value="onTabChange"
        >
          <q-tab
            class="text-teal"
            name="competence-relations"
            label="1.1. Связь с компетенциями"
          />
          <q-tab
            class="text-teal"
            name="competence-indicators"
            label="2. Индикаторы достижения"
          />
          <q-tab
            class="text-teal"
            name="indicator-disciplines"
            label="2.1. Индикаторы и дисциплины"
          />
          <q-tab
            class="text-teal"
            name="indicator-results"
            label="2.2. Результаты обучения"
          />
          <q-tab
            class="text-teal"
            name="assessment-criteria"
            label="3. Критерии оценивания"
          />
        </q-tabs>
      </div>

      <!-- Динамический контент по разделам -->
      <div v-if="loading" class="text-center q-pa-lg">
        <q-spinner color="primary" size="2em" />
        <div class="text-caption q-mt-sm">Загрузка данных...</div>
      </div>

      <div v-else class="section-content">
        <component
          v-if="currentSectionComponent"
          :is="currentSectionComponent"
          :plan-data="planData"
          :competence="currentCompetence"
          :plan-id="currentPlanId"
        />
        <div v-else class="text-center q-pa-xl text-grey">
          <q-icon name="error_outline" size="xl" class="q-mb-md" />
          <div class="text-h6">Раздел не найден</div>
          <div class="text-body2 q-mt-sm">Пожалуйста, выберите другой раздел</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, defineAsyncComponent, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCompetencePassportStore } from 'stores/competencePassportStore'
import { storeToRefs } from 'pinia'
import { useQuasar } from 'quasar'

const route = useRoute()
const router = useRouter()
const store = useCompetencePassportStore()
const $q = useQuasar()

const {
  currentPlanId,
  currentPlanCompetences
} = storeToRefs(store)

const loading = ref(false)
const currentCompetence = ref<any>(null)
const planData = ref<any>(null)
const activeTab = ref('competence-relations')

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
  return (route.query.section as string) || ''
})

const currentCompetenceIndex = computed(() => {
  return (route.query.competence as string) || ''
})

const pageTitle = computed(() => {
  return route.meta?.title || 'Паспорт компетенций'
})

const currentSectionComponent = computed(() => {
  if (!selectedSection.value) return null
  return sectionComponents[selectedSection.value] || null
})

function onTabChange (tabName: string) {
  if (!currentCompetenceIndex.value || !currentPlanId.value || tabName === selectedSection.value) {
    return
  }
  
  router.push({
    name: 'competencePassport',
    params: { 
      planId: currentPlanId.value
    },
    query: { 
      section: tabName,
      competence: currentCompetenceIndex.value
    }
  })
}

async function loadPlanData() {
  if (!currentPlanId.value) {
    planData.value = null
    return
  }

  loading.value = true
  try {
    const competencesData = await store.fetchAllCompetences(currentPlanId.value)
    
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
        },
      }
      try {
        const planResponse = await store.fetchPlanDetails(currentPlanId.value)
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

const loadCompetenceData = async (competenceIndex: string) => {
  if (!competenceIndex || !currentPlanId.value) {
    currentCompetence.value = null
    return
  }

  loading.value = true
  try {
    const data = await store.fetchAllCompetences(currentPlanId.value)
    
    const competence = data?.competences?.find(
      (comp: any) => comp.competence_index === competenceIndex
    )
    
    if (competence) {
      currentCompetence.value = competence
    } else {
      currentCompetence.value = null
      console.warn(`Компетенция ${competenceIndex} не найдена в плане ${currentPlanId.value}`)
    }
  } catch (error) {
    console.error('Ошибка загрузки данных компетенции:', error)
    currentCompetence.value = null
  } finally {
    loading.value = false
  }
}

const updateActiveTab = () => {
  if (selectedSection.value && selectedSection.value !== 'title-page') {
    activeTab.value = selectedSection.value
  }
}

watch(
  () => route.query,
  async (newQuery) => {
    
    if (newQuery.section === 'title-page') {
      await loadPlanData()
      currentCompetence.value = null
    } else if (newQuery.competence) {
      await loadCompetenceData(newQuery.competence as string)
    } else {
      currentCompetence.value = null
    }

    await nextTick()
    updateActiveTab()
  },
  { immediate: true, deep: true }
)

watch(
  () => currentCompetenceIndex.value,
  async (newCompetenceIndex) => {
    if (newCompetenceIndex && currentPlanId.value) {
      await loadCompetenceData(newCompetenceIndex)
    }
  }
)

watch(
  () => selectedSection.value,
  () => {
    updateActiveTab()
  }
)

watch(
  () => currentPlanId.value,
  async (newPlanId) => {
    if (newPlanId) {
      if (route.query.section === 'title-page') {
        await loadPlanData()
      } else if (route.query.competence) {
        await loadCompetenceData(route.query.competence as string)
      }
    } else {
      currentCompetence.value = null
      planData.value = null
    }
    
    await nextTick()
    updateActiveTab()
  }
)

onMounted(async () => {
  
  if (route.query.section === 'title-page' && currentPlanId.value) {
    await loadPlanData()
  } else if (route.query.competence && currentPlanId.value) {
    await loadCompetenceData(route.query.competence as string)
  }
  
  await nextTick()
  updateActiveTab()
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
  
  .competence-tabs {
    .q-tabs {
      .q-tab {
        text-transform: none;
      }
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