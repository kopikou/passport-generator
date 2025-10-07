<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import _ from "lodash";
import LayoutHCF from "components/LayoutHCF.vue";
import useMainStore from "stores/mainStore";
import {storeToRefs} from "pinia";
import {useQuasar} from "quasar";

const props = defineProps({
  id: {
    required: true,
  }
});

const mainStore = useMainStore();
const {
  userId,
} = storeToRefs(mainStore);

const indPlan = ref();

const isAuthor = computed(() => {
  return indPlan.value.plan.user_created.user_id === userId.value;
});

const canAccepted = computed(() => {
  return indPlan.value.plan.zav === userId.value;
});

const canEdit = computed(() => {
  return isAuthor.value && indPlan.value.plan.status === 0;
})

const statuses = [
  {
    title: "Создан",
    color: "grey"
  },
  {
    title: "Ожидает рассмотрения",
    color: "orange-5"
  },
  {
    title: "Утвержден",
    color: "green"
  },
  {
    title: "Требуются правки",
    color: "red-5"
  },
];

const controlButtons = [
  {
    label: "Утвердить",
    permission: canAccepted,
    current_statuses: [1],
    next_status: 2,
    color: "green",
    icon: "mdi-check",
    text_color: "black",
  },
  {
    label: "Отправить на доработку",
    permission: canAccepted,
    current_statuses: [1],
    next_status: 3,
    color: "red",
    icon: "mdi-repeat",
    text_color: "black",
  },
  {
    label: "Отправить на проверку",
    permission: isAuthor,
    current_statuses: [0, 3],
    next_status: 1,
    color: "orange-4",
    icon: "mdi-send-check-outline",
    text_color: "black",
  },
  {
    label: "Вернуть в редактирование",
    permission: isAuthor,
    current_statuses: [1],
    next_status: 0,
    color: "grey",
    icon: "mdi-pencil",
    text_color: "black",
  },
];

const $q = useQuasar();

async function getIndPlan(){
  const loadProgram = $q.loading.show({
    group: 'programs',
    message: 'Загрузка индивидуального плана',
  });

  const r = await api.get(`/api/indplan/${props.id}/`);
  indPlan.value = r.data;

  loadProgram();
}

onBeforeMount(async() => {
  await getIndPlan();
  await getWorks();
});

async function changeStatus(nextStatus: Number) {
  const formData = new FormData();
  formData.append('status', nextStatus.toString());

  const r  = await api.put(`/api/indplan/${props.id}/`, formData);

  indPlan.value.plan.status = r.data.status;
}

const works = ref();

async function getWorks(){
  let r = await api.get(`/api/indplan/get-works/`);
  works.value = r.data;
}

const rows = computed(() =>{
  const typesList = [...new Set(works.value.map(item => item.type))];
  let data = _(typesList)
      .map(item => {
        return {
          type: item,
          works: _(works.value)
              .filter(x => {
                return x.type === item;
              })
              .map(x => {
                const work = _(indPlan.value.works).filter(y => { return y.work !== null && y.work.id === x.id }).value();
                if (x.is_multiple) {
                  if (work.length > 0) {
                    x['count_required'] = work[0].count_required;
                    x['plan_work'] = work[0].id;
                    x['color'] = 'lightgreen';
                  } else {
                    x['count_required'] = 0;
                    x['plan_work'] = -1;
                    x['color'] = '';
                  }
                } else {
                  if (work.length > 0) {
                    x['plan_work'] = work[0].id;
                    x['to_done'] = true;
                    x['color'] = 'lightgreen';
                  } else {
                    x['plan_work'] = -1;
                    x['to_done'] = false;
                    x['color'] = '';
                  }
                }

                return x;
              })
              .value()
        };
      })
      .value();
  return data;
});

const workToAdd = ref(null);
const inputIsActive = ref(true);

async function addUpdateWork(id: number = -1, count_required: number = -1, work_id: number = -1){
  inputIsActive.value = false;

  const formData = new FormData();

  if (work_id > -1) {
    formData.append('work_id', work_id.toString());
  }

  if (workToAdd.value !== null) {
    formData.append('name', workToAdd.value);
    workToAdd.value = null;
  }

  if (count_required > -1 && count_required != '') {
    formData.append('count_required', count_required.toString());
  }

  if (id === -1 && count_required != '') {
    formData.append('plan_id', indPlan.value.plan.id.toString());
    const r = await api.post(`/api/planwork/`, formData);
    indPlan.value.works.push(r.data);
  } else if (id > -1 && count_required > 0) {
    const r = await api.put(`/api/planwork/${id}/`, formData);
    indPlan.value.works.find((item) => item.id === id).count_required = r.data.count_required;
  } else if (id > -1 && count_required <= 0) {
    await deleteWork(id);
  }

    inputIsActive.value = true;
}

async function deleteWork(id: number){
   await api.delete(`/api/planwork/${id}/`);
   const index = indPlan.value.works.findIndex((item) => item.id === id);
   indPlan.value.works.splice(index, 1);
}


</script>

<template>
  <layout-h-c-f v-if="indPlan !== undefined && works !== undefined">
    <template #header>
      <div style="display: grid; grid-template-columns: auto auto auto; gap: 8px; margin: 8px; justify-content: space-between; align-items: center">
        <q-btn label="Назад" icon="mdi-arrow-left" to="/ind_plan/"/>

        <div style="display: grid; grid-template-columns: auto auto auto; gap: 8px; margin: 8px; justify-content: center; align-items: center">
          <span style="font-size: 15px">{{ indPlan.plan.user_created.last_name }} {{ indPlan.plan.user_created.first_name}} {{ indPlan.plan.user_created.middle_name }}, {{indPlan.plan.year}} год</span>
          <q-badge :color="statuses[indPlan.plan.status].color" style="height: 20px; font-size: medium">{{ statuses[indPlan.plan.status].title }}</q-badge>

          <div style="display: flex; gap: 8px; align-items: center; margin: 8px;">
            <div v-for="button in controlButtons">
              <q-btn
                v-if="button.permission.value && button.current_statuses.includes(indPlan.plan.status)"
                :icon="button.icon"
                :color="button.color"
                :text-color="button.text_color"
                @click="changeStatus(button.next_status)"
              >
                <q-tooltip style="font-size: 12px; background-color: white; color: black">
                  {{ button.label }}
                </q-tooltip>
              </q-btn>
            </div>
          </div>
        </div>
      </div>
    </template>

    <template #content>
      <div style="display:grid; grid-template-columns: 5fr 1fr; gap: 12px; padding: 12px" v-if="canEdit">
        <q-input outlined label="Наименогвание работы" v-model="workToAdd"
             clearable @clear="clearFilter"/>

         <q-btn
            label="Добавить"
            style="height: 100%"
            color="primary"
            @click="addUpdateWork()"
           :disable="workToAdd === null"
         />
      </div>

      <div style="display: grid; grid-template-columns: 3fr auto 2fr; gap: 8px">
        <q-list separator>
          <q-expansion-item
              group="somegroup"
              v-for="row in rows"
              :label="row.type"
          >
            <q-separator />
            <q-list style="margin-left: 15px" separator>
              <q-item v-for="work in row.works" :style="'background-color:' + work.color">
                <q-item-section style="display: grid; grid-template-columns: 6fr 3fr; gap: 8px; align-items: center; justify-content: space-between;">
                  <span>{{ work.name }}</span>
                  <div v-if="work.is_multiple" style="display: grid; grid-template-columns: 6fr 1fr; gap: 10px; align-items: center;">
                    <span class="text-right">Количество на исполнение</span>
                    <q-input
                      v-model="work.count_required"
                      type="number"
                      input-class="text-right"
                      dense
                      borderless
                      min="0"
                      :readonly="!canEdit || !inputIsActive"
                      @update:model-value="addUpdateWork(work.plan_work, work.count_required, work.id)"
                    />
                  </div>
                  <div v-else style="display: grid; grid-template-columns: auto auto; gap: 12px; align-items: center; justify-content: end">
                    <span>На исполнение</span>

                    <q-checkbox
                        :disable="!canEdit"
                        v-model="work.to_done"
                        @click="addUpdateWork(work.plan_work, 0, work.id)"
                    />
                  </div>
                </q-item-section>
              </q-item>
            </q-list>
          </q-expansion-item>
        </q-list>

        <q-separator vertical inset />

        <q-list style="display: flex; flex-direction: column; justify-content: start;" separator>
          <span class="text-center">Взятые на исполнение</span>
          <q-item v-for="work in indPlan.works">
            <q-item-section style="display: grid; grid-template-columns: auto 4fr 1fr; gap: 8px; align-items: center; justify-content: space-between">
              <q-btn
                  icon="mdi-trash-can-outline"
                  color="red-4"
                  size="10px"
                  @click="deleteWork(work.id)"
              />

              <span v-if="work.name !== null">{{ work.name }}</span>
              <span v-else>{{ work.work.name }}</span>

              <q-input
                  v-if="work.work !== null && work.work.is_multiple"
                  v-model="work.count_required"
                  input-class="text-right"
                  type="number"
                  dense
                  borderless
                  min="0"
                  :readonly="!canEdit"
                  @update:model-value="addUpdateWork(work.id, work.count_required)"
                  :debounce="1000"
              />
            </q-item-section>
          </q-item>
        </q-list>
      </div>
    </template>
  </layout-h-c-f>
</template>

<style scoped lang="scss">
</style>
