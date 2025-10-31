<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import {api} from "boot/axios";
import _ from "lodash";
import LayoutHCF from "components/LayoutHCF.vue";
import useMainStore from "stores/mainStore";
import {storeToRefs} from "pinia";
import {useQuasar} from "quasar";
import dayjs from "dayjs";

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
  return isAuthor.value && (indPlan.value.plan.status === 0 || indPlan.value.plan.status === 3);
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

const statusToNext = ref();
const newComment = ref('');

async function changeStatus() {
  const formData = new FormData();
  formData.append('status', statusToNext.value.toString());
  if (newComment.value !== '') {
    formData.append('comment', newComment.value);
  }

  const r  = await api.put(`/api/indplan/${props.id}/`, formData);

  indPlan.value.plan.status = r.data.status;
  if (r.data.plan_comment !== null) {
    indPlan.value.plan.comments.push(r.data.plan_comment);
  }

  statusToNext.value = 0;

  newComment.value = '';
}

const works = ref();

async function getWorks(){
  let r = await api.get(`/api/indplan/get-works/`);
  works.value = r.data;
}

const workFilter= ref('');

const rows = computed(() =>{
  let filter = workFilter.value.trim().toLowerCase();
  const typesList = [...new Set(works.value.map(item => item.type))];
  let data = _(typesList)
      .map(item => {
        let hasSelectedWorks = false;
        const itemWorks = _(works.value)
              .filter(x => {
                return x.type === item && x.name.toLowerCase().includes(filter);
              })
              .map(x => {
                const work = _(indPlan.value.works).filter(y => { return y.work !== null && y.work.id === x.id }).value();
                if (x.is_multiple) {
                  if (work.length > 0) {
                    x['count_required'] = work[0].count_required;
                    x['plan_work'] = work[0].id;
                    x['color'] = 'lightgreen';
                    hasSelectedWorks = true;
                  } else {
                    x['count_required'] = 0;
                    x['plan_work'] = -1;
                    x['color'] = 'white';
                  }
                } else {
                  if (work.length > 0) {
                    x['plan_work'] = work[0].id;
                    x['to_done'] = true;
                    x['color'] = 'lightgreen';
                    hasSelectedWorks = true;
                  } else {
                    x['plan_work'] = -1;
                    x['to_done'] = false;
                    x['color'] = 'white';
                  }
                }

                return x;
              })
              .value();
        return {
          type: item,
          works: itemWorks,
          color: hasSelectedWorks ? 'lightgreen' : 'white'
        };
      })
      .value();
  data = data.filter(item => {return item.works.length > 0});
  return data;
});

const indPlanWorks = computed(() => {
  const typesList = [...new Set(indPlan.value.works.map(item => {
    if (item.work !== null)
      return item.work.type
    else
      return item.type
  }))];

  let id = 0;

  let data = _(typesList)
    .map(item => {
      return {
        type: item,
        works: _(indPlan.value.works)
          .filter(work => {
            if (work.work !== null)
              return work.work.type === item
            else
              return work.type === item
          })
          .map(x => {
            id += 1
            return {
              index: id,
              value: x
            }
          })
          .value()
      }
    })
    .value();

  return data;
});

const typesList = [
  'Научно-исследовательская работа',
  'Организационно-методическая работа',
  'Работа по воспитанию обучающихся',
  'Повышение квалификации',
  'Работа с обучающимися и абитуриентами',
  'Учебно-методическая работа'
];

const workToAdd = ref('');
const typeToAdd = ref(null);

const addWorkDialog = ref(false);
const changeStatusDialog = ref(false);
const viewCommentDialog = ref(false);
const addCommentToWorkDialog = ref(false);

const currentWork = ref(null);

async function createWork() {
  const formData = new FormData();

  formData.append('name', workToAdd.value.toString());
  formData.append('type', typeToAdd.value.toString());
  formData.append('plan_id', indPlan.value.plan.id.toString());

  const r = await api.post(`/api/planwork/`, formData);

  indPlan.value.works.push(r.data);
}

async function addWork(work_id: number) {
    const formData = new FormData();

    formData.append('work_id', work_id.toString());
    formData.append('plan_id', indPlan.value.plan.id.toString());

    const r = await api.post(`/api/planwork/`, formData);

    indPlan.value.works.push(r.data);
}

async function updateWork() {
  const formData = new FormData();

  formData.append('additional_info', currentWork.value.additional_info.toString());
  const r = await api.put(`/api/planwork/${currentWork.value.id}/`, formData);

  currentWork.value = null;
}

async function deleteWork(id: number){
  $q.loading.show();
   await api.delete(`/api/planwork/${id}/`);
   const index = indPlan.value.works.findIndex((item) => item.id === id);
   indPlan.value.works.splice(index, 1);
   $q.loading.hide()
}
</script>

<template>
  <layout-h-c-f v-if="indPlan !== undefined && works !== undefined">
    <template #header>
      <div style="display: grid; grid-template-columns: auto auto auto; gap: 8px; margin: 8px; justify-content: space-between; align-items: center">
        <q-btn label="Назад" icon="mdi-arrow-left" to="/ind_plan/"/>

        <div style="display: grid; grid-template-columns: auto auto auto auto; gap: 8px; margin: 8px; justify-content: center; align-items: center">
          <span style="font-size: 15px">{{ indPlan.plan.user_created.last_name }} {{ indPlan.plan.user_created.first_name}} {{ indPlan.plan.user_created.middle_name }}, {{ indPlan.plan.additional_info.doljn }}, ставка {{ indPlan.plan.additional_info.rate }}, {{indPlan.plan.year}} год</span>
          <q-badge
            :color="statuses[indPlan.plan.status].color"
            style="height: 20px; font-size: medium">
            {{ statuses[indPlan.plan.status].title }}
          </q-badge>

          <q-btn
            v-if="indPlan.plan.comments.length > 0"
            icon="mdi-message-text-outline"
            color="primary"
            @click="viewCommentDialog = true"
          >
            <q-tooltip style="font-size: 12px; background-color: white; color: black">
              Посмотреть комментарии
            </q-tooltip>
          </q-btn>

          <div style="display: flex; gap: 8px; align-items: center; margin: 8px;">
            <div v-for="button in controlButtons">
              <q-btn
                v-if="button.permission.value && button.current_statuses.includes(indPlan.plan.status)"
                :icon="button.icon"
                :color="button.color"
                :text-color="button.text_color"
                @click="statusToNext = button.next_status; (button.next_status === 3 || indPlan.plan.status === 3) ? changeStatusDialog = true : changeStatus()"
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

      <div style="display: grid; grid-template-columns: 5fr 1fr; gap: 8px; margin: 8px">
        <q-input
          outlined
          label="Наименование работы"
          v-model="workFilter"
          clearable
          @clear="workFilter = ''"
        />

        <q-btn
          label="Добавить работу"
          style="height: 100%"
          color="primary"
          @click="addWorkDialog = true"
          :disable="!canEdit"
        />
      </div>

      <div style="display: grid; grid-template-columns: 4fr auto 4fr; gap: 8px; margin: 10px">
        <q-list separator>
          <q-expansion-item
              group="somegroup"
              v-for="(row, index) in rows"
              :label="row.type"
              :default-opened="index === 0"
              :style="'background-color:' + row.color"
          >
            <q-separator />
            <q-list style="margin-left: 15px" separator>
              <q-item v-for="work in row.works" :style="'background-color:' + work.color">
                <q-item-section style="display: grid; grid-template-columns: 6fr 3fr; gap: 8px; align-items: center; justify-content: space-between;">
                  <span>{{ work.name }}</span>

                  <div style="display: grid; grid-template-columns: auto auto; gap: 12px; align-items: center; justify-content: end">
                    <span>На исполнение</span>

                    <q-checkbox
                        :disable="!canEdit || work.to_done"
                        v-model="work.to_done"
                        @click="addWork(work.id)"
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
          <q-item v-for="type in indPlanWorks" style="display: flex; flex-direction: column">
            <span class="text-center">{{ type.type }}</span>
            <q-item-section
              v-for="work in type.works"
              style="display: grid; grid-template-columns:10fr 2fr 1fr; gap: 8px; align-items: center; justify-content: space-between; margin-left: 0; margin-bottom: 12px"
            >
              <div style="display: flex; flex-direction: column; gap: 6px">
                <span v-if="work.value.name !== null">{{ work.index }}) {{ work.value.name }}</span>
                <span v-else>{{ work.index }}) {{ work.value.work.name }}</span>

                <span style="color: dimgrey; font-size: small; white-space: pre-wrap">{{work.value.additional_info}}</span>
              </div>

              <div v-show="canEdit">
                <q-btn
                  icon="mdi-message-text-outline"
                  color="secondary"
                  size="10px"
                  @click="currentWork = work.value; addCommentToWorkDialog = true"
                  style="margin-inline: 8px"
                />
                <q-btn
                    icon="mdi-trash-can-outline"
                    color="red-4"
                    size="10px"
                    @click="deleteWork(work.value.id)"
                    style="margin-inline: 8px"
                />
              </div>
            </q-item-section>
          </q-item>
        </q-list>
      </div>

      <q-dialog v-model="addWorkDialog" persistent>
        <q-card style="min-width: 500px">
          <q-card-section>
            <div class="text-h6">Добавление работы</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-input
              outlined
              type="text"
              label="Наименование работы"
              v-model="workToAdd"
              autofocus
            />

            <q-select v-model="typeToAdd"
              label="Тип работы"
              :options="typesList"
              emit-value
              map-options
              clearable
            />
          </q-card-section>

          <q-card-actions align="right" class="text-primary">
            <q-btn
              color="red-5"
              label="Отмена"
              v-close-popup
              @click="workToAdd = ''; typeToAdd = null"
            />
            <q-btn
              color="primary"
              label="Добавить"
              v-close-popup
              @click="createWork()"
              :disable="workToAdd === '' || typeToAdd === null"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <q-dialog v-model="changeStatusDialog" persistent>
        <q-card style="min-width: 500px">
          <q-card-section>
            <div class="text-h6">Смена статуса</div>
          </q-card-section>

          <q-card-section
            class="q-pt-none"
            v-if="indPlan.plan.comments.length > 0"
            style="display: flex; flex-direction: column;"
          >
            Предыдущие комментарии:
            <div v-for="comment in indPlan.plan.comments" style="display: flex; flex-direction: column">
              <span style="align-self: start;">{{ comment.comment }}</span>
              <span style="align-self: end; color: dimgrey" v-if="comment.author !== null && comment.date !== null"> - {{ comment.author.last_name }} {{ comment.author.first_name.substring(0, 1) }}.{{ comment.author.middle_name.substring(0, 1) }}., {{ dayjs(comment.date).format('DD.MM.YYYY, HH:mm') }}</span>
              <q-separator/>
            </div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-input
              outlined
              type="textarea"
              label="Комментарий"
              v-model="newComment"
              autofocus
            />
          </q-card-section>

          <q-card-actions align="right" class="text-primary">
            <q-btn
              color="red-5"
              label="Отмена"
              v-close-popup
              @click="newComment = ''"
            />
            <q-btn
              color="primary"
              label="Отправить"
              v-close-popup
              @click="changeStatus()"
              :disable="newComment === ''"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <q-dialog v-model="viewCommentDialog">
        <q-card style="min-width: 500px">
          <q-card-section>
            <div class="text-h6">Комментарии</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <div v-for="comment in indPlan.plan.comments" style="display: flex; flex-direction: column">
              <span style="align-self: start;">{{ comment.comment }}</span>
              <span style="align-self: end; color: dimgrey" v-if="comment.author !== null && comment.date !== null"> - {{ comment.author.last_name }} {{ comment.author.first_name.substring(0, 1) }}.{{ comment.author.middle_name.substring(0, 1) }}., {{ dayjs(comment.date).format('DD.MM.YYYY, HH:mm') }}</span>
              <q-separator/>
            </div>
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="OK" color="primary" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>

      <q-dialog v-model="addCommentToWorkDialog" persistent>
        <q-card style="min-width: 500px">
          <q-card-section>
            <div class="text-h6">Примечание к работе</div>
          </q-card-section>

          <q-card-section class="q-pt-none">
            <q-input
              outlined
              type="textarea"
              label="Примечание"
              v-model="currentWork.additional_info"
              autofocus
            />
          </q-card-section>

          <q-card-actions align="right" class="text-primary">
            <q-btn
              color="red-5"
              label="Отмена"
              v-close-popup
              @click="currentWork = null; addCommentToWorkDialog = false"
            />
            <q-btn
              color="primary"
              label="Добавить"
              v-close-popup
              @click="updateWork()"
              :disable="currentWork.additional_info === null"
            />
          </q-card-actions>
        </q-card>
      </q-dialog>

    </template>
  </layout-h-c-f>
</template>

<style scoped lang="scss">
</style>
