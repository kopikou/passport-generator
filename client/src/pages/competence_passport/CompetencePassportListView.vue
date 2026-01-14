<template>
  <layout-h-c-f>
    <template #header>
      <div class="q-px-sm q-pb-sm">
        <div class="flex justify-between q-my-sm q-px-sm"
             style="display: grid; grid-template-columns: 1fr 220px auto auto; gap: 8px; align-items: center;">
          <q-input 
            outlined 
            label="Поиск по направлению, аббревиатуре, специальности, коду и т.д." 
            v-model="groupTextFilter" 
            clearable
            @update:model-value="handleSearchChange"
          />
          <q-select
            v-model="selectedYear"
            label="Год"
            :options="yearsList"
            @update:model-value="handleYearChange"
          />
        </div>
      </div>
    </template>
    <template #content>
      <div v-if="groupsList.length > 0"
           style="display: grid; grid-template-columns: 300px 1fr; overflow: hidden; height: 100%"
      >
        <!-- Левая панель со списком групп -->
        <q-list
          style="overflow-y: auto; height: 100%; box-shadow: 0 0 8px silver; z-index: 100"
          separator
        >
          <q-item
            v-for="group in filteredGroups"
            :key="group.plan_id"
            style="display: grid; gap: 8px;"
            clickable
            :active="currentPlanId === group.plan_id"
            @click="selectGroup(group.plan_id)"
            active-class="my-active-item"
          >
            <div style="display: grid; grid-template-columns: 1fr auto">
              <div style="display: flex; justify-content: left; font-size: 1.25rem;">
                {{ `${group.abbr}-${group.yr.toString().slice(-2)}` }}
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr auto">
              <a :href="getFirstPlxFile(group.plx_file)" v-if="getFirstPlxFile(group.plx_file)">*.plx</a>
            </div>
          </q-item>
        </q-list>

        <!-- Правая панель с выбором действия -->
        <div v-if="currentPlanId" style="display: flex; flex-direction: column; height: 100%; padding: 20px;">
          <div class="text-h5 q-mb-md">Выберите действие для группы</div>
          
          <!-- Карточки выбора действия -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <!-- Загрузка нового учебного плана -->
            <q-card class="cursor-pointer" @click="uploadPlan">
              <q-card-section>
                <div class="text-h6">Загрузить учебный план</div>
                <div class="text-caption text-grey">
                  Загрузите новый файл учебного плана в формате .plx
                </div>
              </q-card-section>
              <q-card-actions>
                <q-btn color="primary" label="Загрузить" @click.stop="uploadPlan" />
              </q-card-actions>
            </q-card>

            <!-- Выбор существующего учебного плана -->
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

        <span
          v-else
          style="align-content: center; text-align: center; font-size: 20px; font-weight: bold"
        >
          Выберите нужный раздел слева
        </span>
      </div>

    </template>
  </layout-h-c-f>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useCompetencePassportStore } from 'stores/competencePassportStore';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia'
import { LocalStorage, useQuasar } from 'quasar';
import _ from 'lodash';
import LayoutHCF from 'components/LayoutHCF.vue';
import dayjs from "dayjs";

const store = useCompetencePassportStore()
const {
  groupsList,
  currentPlanId,
  groupTextFilter,
  textFilter,
  statusFilter,
  myFilter,
  selectedYear
} = storeToRefs(store)
const router = useRouter()
const $q = useQuasar()

const yearsList = computed(() => {
  let year = 2025;
  let list = []
  while (year <= dayjs().year() + 1) {
    list.push(year);
    year += 1;
  }
  return list;
});

const filteredGroups = computed(() => {
  if (!groupTextFilter.value || groupTextFilter.value.trim() === '') {
    return groupsList.value;
  }
  
  const searchLower = groupTextFilter.value.toLowerCase().trim();
  
  return groupsList.value.filter(group => {
    const fieldsToSearch = [
      group.abbr,
      group.yr?.toString(),
      group.dir, 
      group.sp,
      group.kod, 
      group.spec, 
      group.name, 
    ];
    
    const fullMatchFields = [
      `${group.abbr}-${group.yr?.toString()?.slice(-2)}`,
    ];
    
    for (const field of fieldsToSearch) {
      if (field && field.toString().toLowerCase().includes(searchLower)) {
        return true;
      }
    }
    
    for (const field of fullMatchFields) {
      if (field && field.toLowerCase().includes(searchLower)) {
        return true;
      }
    }
    
    if (group.dir && typeof group.dir === 'object') {
      if (group.dir.name && group.dir.name.toLowerCase().includes(searchLower)) {
        return true;
      }
      if (group.dir.code && group.dir.code.toLowerCase().includes(searchLower)) {
        return true;
      }
    }
    
    return false;
  });
});

function getFirstPlxFile(plxFile) {
  if (!plxFile) return null;
  if (Array.isArray(plxFile) && plxFile.length > 0) {
    return plxFile[0];
  }
  return plxFile;
}

function handleSearchChange() {
  if (groupTextFilter.value && groupTextFilter.value.trim() !== '') {
    LocalStorage.set('surp_rpdgroupfilter', groupTextFilter.value);
  } else {
    LocalStorage.remove('surp_rpdgroupfilter');
  }
  debouncedFetchGroupsList();
}

function handleYearChange() {
  debouncedFetchGroupsList();
}

const debouncedFetchGroupsList = _.debounce(async () => {
  await store.fetchGroupsList();
}, 300);

async function selectGroup(planId) {
  store.setCurrentPlanId(planId);
}

function uploadPlan() {
  $q.notify({
    type: 'info',
    message: 'Функция загрузки будет реализована позже'
  });
}

function selectExistingPlan() {
  if (!currentPlanId.value) {
    $q.notify({
      type: 'warning',
      message: 'Выберите группу'
    });
    return;
  }
  
  router.push(`/competence/reference`);
}

onMounted(async () => {
  const savedFilter = LocalStorage.getItem('surp_rpdgroupfilter');
  if (savedFilter !== null && savedFilter !== undefined && savedFilter !== 'null') {
    groupTextFilter.value = savedFilter;
  } else {
    groupTextFilter.value = '';
    LocalStorage.remove('surp_rpdgroupfilter');
  }
  
  await store.fetchGroupsList();
})

watch([textFilter, statusFilter, myFilter], _.debounce(async () => {
  await store.fetchGroupsList();
}, 300))
</script>

<style scoped lang="scss">
:deep(.table-header) {
  position: sticky;
  z-index: 1;
  top: 0;
  background: $blue-grey-2;
}

:deep(.my-active-item) {
  background: $blue-grey-2;
}
</style>