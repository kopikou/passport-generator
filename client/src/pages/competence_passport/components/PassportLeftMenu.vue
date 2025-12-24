<template>
  <div class="competence-menu">
    <div class="menu-header q-pa-sm bg-grey-3">
      <div class="text-weight-bold">Компетенции</div>
      <div class="text-caption text-grey q-mb-sm">
        Всего: {{ filteredCompetences.length }}
      </div>
      
      <!-- Поиск и фильтры -->
      <div class="q-gutter-y-sm">
        <q-input
          v-model="searchText"
          placeholder="Поиск по индексу..."
          dense
          outlined
          clearable
          class="bg-white"

        >
          <template v-slot:prepend>
            <q-icon name="search" />
          </template>
        </q-input>
        
        <q-select
          v-model="selectedType"
          :options="competenceTypes"
          label="Фильтр по типу"
          dense
          outlined
          clearable
          emit-value
          map-options
          class="bg-white"

        />
      </div>
    </div>

    <div v-if="loading" class="q-pa-lg text-center">
      <q-spinner color="primary" size="2em" />
      <div class="text-caption q-mt-sm">Загрузка компетенций...</div>
    </div>

    <!-- Список компетенций -->
    <q-list class="competence-list" dense>
      <div v-if="filteredCompetences.length === 0" class="text-center q-py-lg text-grey">
        <div v-if="searchText || selectedType">Компетенции не найдены</div>
        <div v-else>Компетенции не загружены</div>
      </div>

      <!-- Титульный лист -->
      <q-item 
        clickable
        v-ripple
        class="title-page-header"
        @click="navigateToTitlePage"
        :active="isTitlePageActive()"
        active-class="bg-amber-2 text-black"
        dense
      >
        <q-item-section>
          <q-item-label class="text-weight-medium">
            Титульный лист
          </q-item-label>
        </q-item-section>
      </q-item>

      <!-- Компетенции -->
      <q-item
        v-for="comp in filteredCompetences"
        :key="comp.competence_index"
        clickable
        v-ripple
        class="competence-header"
        :class="getCompetenceClass(comp.competence_index)"
        @click="navigateToCompetence(comp)"
        :active="isCompetenceActive(comp)"
        active-class="bg-amber-2 text-black"
      >
        <q-item-section>
          <q-item-label class="text-weight-medium">
            {{ comp.competence_index }}
          </q-item-label>
        </q-item-section>
        <q-item-section side>
          <q-badge :color="getTypeBadgeColor(comp.competence_index)" rounded>
            {{ getCompetenceType(comp.competence_index) }}
          </q-badge>
        </q-item-section>
      </q-item>
    </q-list>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCompetencePassportStore } from 'stores/competencePassportStore'
import { storeToRefs } from 'pinia'
import { useQuasar } from 'quasar'

const router = useRouter()
const $route = useRoute()
const store = useCompetencePassportStore()
const {
  currentPlanId,
  currentPlanCompetences,
} = storeToRefs(store)

const $q = useQuasar()

const searchText = ref('')
const selectedType = ref('')
const loading = ref(false)
const competencesData = ref([])

// Типы компетенций для фильтра
const competenceTypes = [
  { label: 'Универсальные (УК)', value: 'Универсальная' },
  { label: 'Общепрофессиональные (ОПК)', value: 'Общепрофессиональная' },
  { label: 'Профессиональные (ПК)', value: 'Профессиональная' },
  { label: 'Дополнительные (ДК)', value: 'Дополнительная' },
  { label: 'Другие', value: 'Другая' }
]

// Определяем тип компетенции по индексу
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

const getTypeBadgeColor = (competenceIndex) => {
  const type = getCompetenceType(competenceIndex)
  const colors = {
    'Универсальная': 'blue',
    'Общепрофессиональная': 'green',
    'Профессиональная': 'orange',
    'Дополнительная': 'purple',
    'Другая': 'grey'
  }
  return colors[type] || 'grey'
}

const getCompetenceClass = (competenceIndex) => {
  const type = getCompetenceType(competenceIndex)
  return `competence-${type.toLowerCase().replace(/ /g, '-')}`
}

const isTitlePageActive = () => {
  return $route.query.section === 'title-page'
}

const isCompetenceActive = (competence) => {
  return $route.query.competence === competence.competence_index && 
         $route.query.section && 
         $route.query.section !== 'title-page'
}

const filteredCompetences = computed(() => {
  let competences = competencesData.value
  
  if (searchText.value) {
    const searchLower = searchText.value.toLowerCase()
    competences = competences.filter(comp => 
      comp.competence_index.toLowerCase().includes(searchLower) ||
      comp.competence.toLowerCase().includes(searchLower)
    )
  }
  
  if (selectedType.value) {
    competences = competences.filter(comp => 
      getCompetenceType(comp.competence_index) === selectedType.value
    )
  }
  
  return competences
})

// const handleSearch = () => {
//   // Поиск не требует дополнительных действий
// }

// const handleTypeFilter = () => {
//   // Фильтрация не требует дополнительных действий
// }

const navigateToTitlePage = () => {
  router.push({
    name: 'competencePassport',
    params: { 
      planId: currentPlanId.value
    },
    query: { 
      section: 'title-page'
    }
  })
}

const navigateToCompetence = (competence) => {
  router.push({
    name: 'competencePassport',
    params: { 
      planId: currentPlanId.value
    },
    query: { 
      section: 'competence-relations',
      competence: competence.competence_index 
    }
  })
}

const loadCompetences = async () => {
  if (!currentPlanId.value) {
    competencesData.value = []
    return
  }

  loading.value = true
  try {
    const data = await store.fetchAllCompetences(currentPlanId.value)
    if (data && data.competences) {
      competencesData.value = data.competences
    } else {
      competencesData.value = []
    }
  } catch (error) {
    console.error('Error loading competences:', error)
    $q.notify({
      type: 'negative',
      message: 'Ошибка загрузки компетенций',
      position: 'top-right'
    })
    competencesData.value = []
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  if (currentPlanId.value) {
    await loadCompetences()
  }
})

watch(() => currentPlanId.value, async (newPlanId) => {
  if (newPlanId) {
    await loadCompetences()
  } else {
    competencesData.value = []
  }
})

watch(() => currentPlanCompetences.value, (newCompetences) => {
  if (newCompetences && newCompetences.length > 0) {
    competencesData.value = newCompetences
  }
}, { deep: true })
</script>

<style scoped lang="scss">
.competence-menu {
  height: 100%;
  display: flex;
  flex-direction: column;
  
  .menu-header {
    border-bottom: 1px solid #e0e0e0;
    flex-shrink: 0;
  }
  
  .competence-list {
    .title-page-header {
      border-bottom: 1px solid rgba(0,0,0,0.05);
      min-height: 50px;
    }

    .competence-header {
      border-bottom: 1px solid rgba(0,0,0,0.05);
      min-height: 50px;
      
      .q-item__label {
        line-height: 1.3;
      }
    }
  }
}

.q-badge {
  font-size: 10px;
  padding: 2px 6px;
  font-weight: 500;
}

:deep(.q-scrollarea__content) {
  width: 100%;
}
</style>