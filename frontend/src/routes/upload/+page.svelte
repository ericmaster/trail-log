<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { api, type UploadMetadata, type UploadResponse } from "$lib/api";
  import { t } from "svelte-i18n";
  import LanguageSwitcher from "$lib/components/LanguageSwitcher.svelte";
  import InfoTooltip from "$lib/components/InfoTooltip.svelte";

  let file: File | null = null;
  let sessionType = "";
  let raceName = "";
  let notes = "";
  let fatigueLevel: number | undefined;
  let generalSensation: number | undefined;
  let sleepQuality: number | undefined;
  let hydrationStatus = "";
  let weatherCondition = "";
  let trailCondition = "";

  let error = "";
  let success = "";
  let loading = false;
  let uploads: UploadResponse[] = [];
  let isDragging = false;

  onMount(() => {
    if (!api.isAuthenticated()) {
      goto("/login");
      return;
    }
    loadUploads();
  });

  async function loadUploads() {
    try {
      uploads = await api.listUploads();
    } catch (e) {
      console.error("Failed to load uploads:", e);
    }
  }

  function handleFileSelect(event: Event) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files[0]) {
      file = input.files[0];
    }
  }

  function handleDrop(event: DragEvent) {
    event.preventDefault();
    isDragging = false;
    if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
      const droppedFile = event.dataTransfer.files[0];
      if (droppedFile.name.toLowerCase().endsWith(".fit")) {
        file = droppedFile;
      } else {
        error = $t("upload.only_fit");
      }
    }
  }

  function handleDragOver(event: DragEvent) {
    event.preventDefault();
    isDragging = true;
  }

  function handleDragLeave() {
    isDragging = false;
  }

  async function handleUpload() {
    if (!file) {
      error = $t("upload.please_select");
      return;
    }

    error = "";
    success = "";
    loading = true;

    try {
      const metadata: UploadMetadata = {
        session_type: sessionType || undefined,
        race_name: raceName || undefined,
        notes: notes || undefined,
        fatigue_level: fatigueLevel,
        general_sensation: generalSensation,
        sleep_quality: sleepQuality,
        hydration_status: hydrationStatus || undefined,
        weather_condition: weatherCondition || undefined,
        trail_condition: trailCondition || undefined,
      };

      await api.uploadFile(file, metadata);
      success = `${$t("upload.success")} ${file.name}`;

      // Reset form
      file = null;
      sessionType = "";
      raceName = "";
      notes = "";
      fatigueLevel = undefined;
      generalSensation = undefined;
      sleepQuality = undefined;
      hydrationStatus = "";
      weatherCondition = "";
      trailCondition = "";

      // Reload uploads list
      await loadUploads();
    } catch (e) {
      error = e instanceof Error ? e.message : $t("upload.failed");
    } finally {
      loading = false;
    }
  }

  function handleLogout() {
    api.logout();
    goto("/login");
  }

  function formatDate(dateStr: string): string {
    return new Date(dateStr).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }
</script>

<svelte:head>
  <title>{$t("upload.title")}</title>
</svelte:head>

<div class="min-vh-100 py-3">
  <div class="container" style="max-width: 900px;">
    <header
      class="d-flex justify-content-between align-items-center mb-4 border-bottom border-secondary pb-3"
    >
      <h1 class="h3 mb-0 text-white">{$t("upload.header")}</h1>
      <div class="d-flex align-items-center gap-2">
        <button class="btn btn-outline-light btn-sm" on:click={handleLogout}
          >{$t("upload.logout")}</button
        >
        <LanguageSwitcher />
      </div>
    </header>

    <main>
      <div class="card bg-dark text-white border-secondary mb-5 shadow">
        <div class="card-body p-4">
          <h2 class="h4 mb-4">{$t("upload.upload_file")}</h2>

          {#if error}
            <div class="alert alert-danger" role="alert">{error}</div>
          {/if}

          {#if success}
            <div class="alert alert-success" role="alert">{success}</div>
          {/if}

          <form on:submit|preventDefault={handleUpload}>
            <!-- File Drop Zone -->
            <div
              class="drop-zone mb-4 p-5 text-center border rounded-3 position-relative"
              class:dragging={isDragging}
              class:has-file={file !== null}
              class:bg-dark-subtle={isDragging}
              class:border-primary={isDragging}
              class:border-success={file !== null}
              on:drop={handleDrop}
              on:dragover={handleDragOver}
              on:dragleave={handleDragLeave}
              role="button"
              tabindex="0"
            >
              {#if file}
                <div
                  class="d-flex align-items-center justify-content-center gap-3"
                >
                  <span class="fs-4">📄</span>
                  <span class="fw-medium">{file.name}</span>
                  <button
                    type="button"
                    class="btn btn-sm btn-danger rounded-circle p-0 d-flex align-items-center justify-content-center"
                    style="width: 24px; height: 24px;"
                    on:click|stopPropagation={() => (file = null)}>×</button
                  >
                </div>
              {:else}
                <input
                  type="file"
                  accept=".fit"
                  on:change={handleFileSelect}
                  id="file-input"
                  class="position-absolute top-0 start-0 w-100 h-100 opacity-0 cursor-pointer"
                />
                <label
                  for="file-input"
                  class="d-flex flex-column align-items-center gap-2 text-white-50 cursor-pointer"
                >
                  <span class="fs-1">📁</span>
                  <span>{$t("upload.drop_file")}</span>
                </label>
              {/if}
            </div>

            <h5 class="border-bottom border-secondary pb-2 mb-3">
              {$t("upload.session_context")}
            </h5>
            <div class="row g-3 mb-3">
              <div class="col-md-4">
                <label for="sessionType" class="form-label"
                  >{$t("upload.session_type")}</label
                >
                <select
                  class="form-select bg-dark text-white border-secondary"
                  id="sessionType"
                  bind:value={sessionType}
                >
                  <option value="">{$t("upload.session_types.select")}</option>
                  <option value="race">{$t("upload.session_types.race")}</option
                  >
                  <option value="training"
                    >{$t("upload.session_types.training")}</option
                  >
                  <option value="recovery"
                    >{$t("upload.session_types.recovery")}</option
                  >
                </select>
              </div>

              <div class="col-md-8">
                <label for="raceName" class="form-label"
                  >{$t("upload.race_name")}</label
                >
                <input
                  type="text"
                  class="form-control bg-dark text-white border-secondary"
                  id="raceName"
                  bind:value={raceName}
                  placeholder="e.g., Ultra Trail Mont Blanc"
                />
              </div>
            </div>

            <div class="mb-4">
              <label for="notes" class="form-label">{$t("upload.notes")}</label>
              <textarea
                class="form-control bg-dark text-white border-secondary"
                id="notes"
                bind:value={notes}
                rows="3"
                placeholder={$t("upload.notes_placeholder")}
              ></textarea>
            </div>

            <h5 class="border-bottom border-secondary pb-2 mb-3">
              {$t("upload.physiological")}
            </h5>

            <h6 class="text-white-50 mb-3">{$t("upload.pre_session")}</h6>
            <div class="row g-3 mb-4">
              <div class="col-md-4">
                <div class="d-flex align-items-center mb-2">
                  <div class="form-label mb-0 text-white-50">
                    {$t("upload.fatigue")}
                  </div>
                  <InfoTooltip text={$t("upload.fatigue_desc")} />
                </div>
                <div class="btn-group w-100" role="group">
                  {#each [1, 2, 3, 4, 5] as level}
                    <input
                      type="radio"
                      class="btn-check"
                      name="fatigue"
                      id="fatigue{level}"
                      autocomplete="off"
                      checked={fatigueLevel === level}
                      on:change={() => (fatigueLevel = level)}
                    />
                    <label
                      class="btn btn-outline-secondary"
                      for="fatigue{level}">{level}</label
                    >
                  {/each}
                </div>
              </div>

              <div class="col-md-4">
                <div class="d-flex align-items-center mb-2">
                  <div class="form-label mb-0 text-white-50">
                    {$t("upload.sleep")}
                  </div>
                  <InfoTooltip text={$t("upload.sleep_desc")} />
                </div>
                <div class="btn-group w-100" role="group">
                  {#each [1, 2, 3, 4, 5] as level}
                    <input
                      type="radio"
                      class="btn-check"
                      name="sleep"
                      id="sleep{level}"
                      autocomplete="off"
                      checked={sleepQuality === level}
                      on:change={() => (sleepQuality = level)}
                    />
                    <label class="btn btn-outline-secondary" for="sleep{level}"
                      >{level}</label
                    >
                  {/each}
                </div>
              </div>

              <div class="col-md-4">
                <div class="d-flex align-items-center mb-2">
                  <label for="hydrationStatus" class="form-label mb-0"
                    >{$t("upload.hydration")}</label
                  >
                  <InfoTooltip text={$t("upload.hydration_desc")} />
                </div>
                <select
                  class="form-select bg-dark text-white border-secondary"
                  id="hydrationStatus"
                  bind:value={hydrationStatus}
                >
                  <option value=""
                    >{$t("upload.hydration_options.select")}</option
                  >
                  <option value="well_hydrated"
                    >{$t("upload.hydration_options.well_hydrated")}</option
                  >
                  <option value="mildly_dehydrated"
                    >{$t("upload.hydration_options.mildly_dehydrated")}</option
                  >
                  <option value="uncertain"
                    >{$t("upload.hydration_options.uncertain")}</option
                  >
                </select>
              </div>
            </div>

            <h6 class="text-white-50 mb-3 mt-4">{$t("upload.post_session")}</h6>
            <div class="row g-3 mb-4">
              <div class="col-md-4">
                <div class="d-flex align-items-center mb-2">
                  <div class="form-label mb-0 text-white-50">
                    {$t("upload.general_sensation")}
                  </div>
                  <InfoTooltip text={$t("upload.general_sensation_desc")} />
                </div>
                <div class="btn-group w-100" role="group">
                  {#each [1, 2, 3, 4, 5] as level}
                    <input
                      type="radio"
                      class="btn-check"
                      name="generalSensation"
                      id="generalSensation{level}"
                      autocomplete="off"
                      checked={generalSensation === level}
                      on:change={() => (generalSensation = level)}
                    />
                    <label
                      class="btn btn-outline-secondary"
                      for="generalSensation{level}">{level}</label
                    >
                  {/each}
                </div>
              </div>
            </div>

            <h5 class="border-bottom border-secondary pb-2 mb-3">
              {$t("upload.environmental")}
            </h5>
            <div class="row g-3 mb-4">
              <div class="col-md-6">
                <div class="d-flex align-items-center mb-2">
                  <label for="weatherCondition" class="form-label mb-0"
                    >{$t("upload.weather")}</label
                  >
                  <InfoTooltip text={$t("upload.weather_desc")} />
                </div>
                <select
                  class="form-select bg-dark text-white border-secondary"
                  id="weatherCondition"
                  bind:value={weatherCondition}
                >
                  <option value="">{$t("upload.weather_options.select")}</option
                  >
                  <option value="sunny"
                    >{$t("upload.weather_options.sunny")}</option
                  >
                  <option value="cloudy"
                    >{$t("upload.weather_options.cloudy")}</option
                  >
                  <option value="rain"
                    >{$t("upload.weather_options.rain")}</option
                  >
                  <option value="fog">{$t("upload.weather_options.fog")}</option
                  >
                  <option value="snow"
                    >{$t("upload.weather_options.snow")}</option
                  >
                  <option value="windy"
                    >{$t("upload.weather_options.windy")}</option
                  >
                </select>
              </div>

              <div class="col-md-6">
                <div class="d-flex align-items-center mb-2">
                  <label for="trailCondition" class="form-label mb-0"
                    >{$t("upload.trail_conditions")}</label
                  >
                  <InfoTooltip text={$t("upload.trail_desc")} />
                </div>
                <select
                  class="form-select bg-dark text-white border-secondary"
                  id="trailCondition"
                  bind:value={trailCondition}
                >
                  <option value="">{$t("upload.trail_options.select")}</option>
                  <option value="dry">{$t("upload.trail_options.dry")}</option>
                  <option value="muddy"
                    >{$t("upload.trail_options.muddy")}</option
                  >
                  <option value="icy">{$t("upload.trail_options.icy")}</option>
                  <option value="rocky"
                    >{$t("upload.trail_options.rocky")}</option
                  >
                  <option value="mixed"
                    >{$t("upload.trail_options.mixed")}</option
                  >
                </select>
              </div>
            </div>

            <button
              type="submit"
              class="btn btn-primary w-100 py-2 fw-bold"
              disabled={loading || !file}
            >
              {loading ? $t("upload.uploading") : $t("upload.upload_button")}
            </button>
          </form>
        </div>
      </div>

      {#if uploads.length > 0}
        <div class="card bg-dark text-white border-secondary shadow">
          <div class="card-header border-secondary bg-transparent py-3">
            <h2 class="h5 mb-0">{$t("upload.recent_uploads")}</h2>
          </div>
          <div class="list-group list-group-flush">
            {#each uploads as upload}
              <div
                class="list-group-item bg-dark text-white border-secondary d-flex align-items-center gap-3 py-3"
              >
                <span class="fs-4">📄</span>
                <div class="flex-grow-1">
                  <div class="fw-medium">{upload.filename}</div>
                  <div class="text-white-50 small mt-1">
                    {formatDate(upload.upload_date)}
                    {#if upload.session_type}
                      <span
                        class="badge bg-primary bg-opacity-25 text-primary-emphasis ms-2 text-capitalize"
                        >{upload.session_type}</span
                      >
                    {/if}
                  </div>
                </div>
              </div>
            {/each}
          </div>
        </div>
      {/if}
    </main>
  </div>
</div>

<style>
  .form-control:focus,
  .form-select:focus {
    background-color: #212529;
    color: #fff;
    border-color: #0d6efd;
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
  }

  .drop-zone {
    border: 2px dashed rgba(255, 255, 255, 0.3);
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.05);
    transition: all 0.2s;
  }

  .drop-zone:hover {
    border-color: rgba(255, 255, 255, 0.5);
    background: rgba(255, 255, 255, 0.08);
  }

  .btn-check:checked + .btn-outline-secondary {
    background-color: #6366f1;
    border-color: #6366f1;
    color: white;
  }

  .cursor-pointer {
    cursor: pointer;
  }
</style>
