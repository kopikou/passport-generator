<script setup lang="ts">
import { ref, computed, watch, onBeforeMount } from 'vue'
import { useRouter } from 'vue-router'
import { useQuasar, LocalStorage } from 'quasar'
import _ from 'lodash'
import LayoutHCF from 'components/LayoutHCF.vue'
import dayjs from 'dayjs'
import { useCompetencePassportStore } from 'src/stores/competencePassportStore'
import { storeToRefs } from 'pinia'

const store = useCompetencePassportStore()
const { currentPlanId} = storeToRefs(store)

const router = useRouter()

const $q = useQuasar()

const groupsList = ref<any[]>([])

const groupTextFilter = ref<string>(LocalStorage.getItem('surp_rpdgroupfilter') || '')
const selectedYear = ref<number>(LocalStorage.getItem('surp_yearfilter') || dayjs().year())

const yearsList = computed(() => {
  const startYear = 2025
  const endYear = dayjs().year() + 1
  return _.range(startYear, endYear + 1)
})

const filteredGroups = computed(() => {
  if (!groupTextFilter.value.trim()) return groupsList.value

  const search = groupTextFilter.value.toLowerCase().trim()
  return groupsList.value.filter(group => {
    const fields = [
      group.abbr,
      group.yr?.toString(),
      group.direct_name,
      group.spec_name,
      group.cdirection__cod,
      group.plan_id?.toString()
    ].filter(Boolean) as string[]

    return fields.some(field => field.toLowerCase().includes(search))
  })
})

async function fetchGroups() {
  const loading = $q.loading.show({ message: 'Загрузка списка групп...' })
  try {
    const params = {
      year: selectedYear.value,
      groupText: groupTextFilter.value.trim() || undefined
    }
    const data = await store.getGroupList(params)
    groupsList.value = data
  } finally {
    loading()
  }
}

const debouncedFetch = _.debounce(fetchGroups, 300)

function saveFilters() {
  LocalStorage.set('surp_rpdgroupfilter', groupTextFilter.value)
  LocalStorage.set('surp_yearfilter', selectedYear.value)
}

function selectGroup(planId: number) {
  currentPlanId.value = planId
  LocalStorage.set('current_plan_id', planId)
}

function uploadPlan() {
  $q.notify({
    type: 'info',
    message: 'Функция загрузки будет реализована позже'
  })
}

function selectExistingPlan() {
  if (!currentPlanId.value) {
    $q.notify({ type: 'warning', message: 'Выберите группу' })
    return
  }
  router.push(`/competence-passport/${currentPlanId.value}/competences`)
}

watch([selectedYear, groupTextFilter], () => {
  saveFilters()
  debouncedFetch()
})

onBeforeMount(async () => {
  await fetchGroups()
  //groupTextFilter.value = ''
})
</script>

<template>
  <layout-h-c-f>
    <template #header>
      <div class="q-px-sm q-pb-sm">
        <div
          class="flex justify-between q-my-sm q-px-sm"
          style="display: grid; grid-template-columns: 1fr 220px; gap: 8px; align-items: center;"
        >
          <q-input
            outlined
            label="Поиск по направлению, аббревиатуре, специальности, коду и т.д."
            v-model="groupTextFilter"
            clearable
            @clear="groupTextFilter = ''; saveFilters()"
            @update:model-value="debouncedFetch"
          />
          <q-select
            v-model="selectedYear"
            label="Год"
            :options="yearsList"
            @update:model-value="() => {}"
          />
        </div>
      </div>
    </template>

    <template #content>
      <div v-if="groupsList.length > 0" style="display: grid; grid-template-columns: 300px 1fr; height: 100%">
        <!-- Список групп -->
        <q-list separator style="overflow-y: auto; height: 100%; box-shadow: 0 0 8px silver">
          <q-item
            v-for="group in filteredGroups"
            :key="group.plan_id"
            clickable
            @click="selectGroup(group.plan_id)"
            :active="currentPlanId === group.plan_id"
            active-class="bg-amber-2"
            style="display: grid; gap: 8px;"
          >
            <div style="display: grid; grid-template-columns: 1fr auto">
              <div style="display: flex; justify-content: left; font-size: 1.25rem;">
                {{ `${group.abbr}-${group.yr.toString().slice(-2)}` }}
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr auto">
              <a :href="group.plx_file" v-if="group.plx_file">*.plx</a>
            </div>
          </q-item>
        </q-list>

        <!-- Правая панель с выбором действия -->
        <div v-if="currentPlanId" style="display: flex; flex-direction: column; padding: 20px;">
          <div class="text-h5 q-mb-md">Выберите действие для группы</div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <!-- Загрузка нового плана -->
            <q-card class="cursor-pointer" @click="uploadPlan">
              <q-card-section>
                <div class="text-h6">Загрузить учебный план</div>
                <div class="text-caption text-grey">Загрузите новый файл учебного плана в формате .plx</div>
              </q-card-section>
              <q-card-actions>
                <q-btn color="primary" label="Загрузить" @click.stop="uploadPlan" />
              </q-card-actions>
            </q-card>

            <!-- Выбор существующего плана -->
            <q-card class="cursor-pointer" @click="selectExistingPlan">
              <q-card-section>
                <div class="text-h6">Выбрать прошлогодний учебный план</div>
                <div class="text-caption text-grey">
                  Данные автоматически подгрузятся из прошлогоднего учебного плана
                </div>
              </q-card-section>
              <q-card-actions>
                <q-btn color="primary" label="Выбрать" @click.stop="selectExistingPlan" />
              </q-card-actions>
            </q-card>
          </div>
        </div>

        <div v-else class="flex flex-center" style="height: 100%">
          <div class="text-h6 text-grey">Выберите нужный раздел слева</div>
        </div>
      </div>

      <div v-else class="flex flex-center" style="height: 100%">
        <div class="text-h6 text-grey">Нет данных</div>
      </div>
    </template>
  </layout-h-c-f>
</template>

<style scoped lang="scss">
:deep(.my-active-item) {
  background: $blue-grey-2;
}
</style>