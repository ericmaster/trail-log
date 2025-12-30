<script lang="ts">
  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import { api, type UploadMetadata, type UploadResponse } from "$lib/api";

  let file: File | null = null;
  let sessionType = "";
  let raceName = "";
  let notes = "";
  let fatigueLevel: number | undefined;
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
        error = "Only .fit files are allowed";
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
      error = "Please select a file";
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
        sleep_quality: sleepQuality,
        hydration_status: hydrationStatus || undefined,
        weather_condition: weatherCondition || undefined,
        trail_condition: trailCondition || undefined,
      };

      await api.uploadFile(file, metadata);
      success = `Successfully uploaded ${file.name}`;

      // Reset form
      file = null;
      sessionType = "";
      raceName = "";
      notes = "";
      fatigueLevel = undefined;
      sleepQuality = undefined;
      hydrationStatus = "";
      weatherCondition = "";
      trailCondition = "";

      // Reload uploads list
      await loadUploads();
    } catch (e) {
      error = e instanceof Error ? e.message : "Upload failed";
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
  <title>Upload - Trail Fit Uploader</title>
</svelte:head>

<div class="min-vh-100 py-3">
  <div class="container" style="max-width: 900px;">
    <header
      class="d-flex justify-content-between align-items-center mb-4 border-bottom border-secondary pb-3"
    >
      <h1 class="h3 mb-0 text-white">Trail Fit Uploader</h1>
      <button class="btn btn-outline-light btn-sm" on:click={handleLogout}
        >Logout</button
      >
    </header>

    <main>
      <div class="card bg-dark text-white border-secondary mb-5 shadow">
        <div class="card-body p-4">
          <h2 class="h4 mb-4">Upload .fit File</h2>

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
                  <span>Drop .fit file here or click to browse</span>
                </label>
              {/if}
            </div>

            <h5 class="border-bottom border-secondary pb-2 mb-3">
              Session Context
            </h5>
            <div class="row g-3 mb-3">
              <div class="col-md-4">
                <label for="sessionType" class="form-label">Session Type</label>
                <select
                  class="form-select bg-dark text-white border-secondary"
                  id="sessionType"
                  bind:value={sessionType}
                >
                  <option value="">Select...</option>
                  <option value="race">Race</option>
                  <option value="training">Training</option>
                  <option value="recovery">Recovery</option>
                </select>
              </div>

              <div class="col-md-8">
                <label for="raceName" class="form-label"
                  >Race Name (if applicable)</label
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
              <label for="notes" class="form-label">Notes / Observations</label>
              <textarea
                class="form-control bg-dark text-white border-secondary"
                id="notes"
                bind:value={notes}
                rows="3"
                placeholder="Any observations about this session..."
              ></textarea>
            </div>

            <h5 class="border-bottom border-secondary pb-2 mb-3">
              Physiological / Subjective
            </h5>
            <div class="row g-3 mb-4">
              <div class="col-md-4">
                <label class="form-label d-block"
                  >Pre-session Fatigue (1-5)</label
                >
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
                <label class="form-label d-block">Sleep Quality (1-5)</label>
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
                <label for="hydrationStatus" class="form-label"
                  >Hydration Status</label
                >
                <select
                  class="form-select bg-dark text-white border-secondary"
                  id="hydrationStatus"
                  bind:value={hydrationStatus}
                >
                  <option value="">Select...</option>
                  <option value="well_hydrated">Well-hydrated</option>
                  <option value="mildly_dehydrated">Mildly dehydrated</option>
                  <option value="uncertain">Uncertain</option>
                </select>
              </div>
            </div>

            <h5 class="border-bottom border-secondary pb-2 mb-3">
              Environmental Conditions
            </h5>
            <div class="row g-3 mb-4">
              <div class="col-md-6">
                <label for="weatherCondition" class="form-label">Weather</label>
                <select
                  class="form-select bg-dark text-white border-secondary"
                  id="weatherCondition"
                  bind:value={weatherCondition}
                >
                  <option value="">Select...</option>
                  <option value="sunny">Sunny</option>
                  <option value="cloudy">Cloudy</option>
                  <option value="rain">Rain</option>
                  <option value="fog">Fog</option>
                  <option value="snow">Snow</option>
                  <option value="windy">Windy</option>
                </select>
              </div>

              <div class="col-md-6">
                <label for="trailCondition" class="form-label"
                  >Trail Conditions</label
                >
                <select
                  class="form-select bg-dark text-white border-secondary"
                  id="trailCondition"
                  bind:value={trailCondition}
                >
                  <option value="">Select...</option>
                  <option value="dry">Dry</option>
                  <option value="muddy">Muddy</option>
                  <option value="icy">Icy</option>
                  <option value="rocky">Rocky</option>
                  <option value="mixed">Mixed</option>
                </select>
              </div>
            </div>

            <button
              type="submit"
              class="btn btn-primary w-100 py-2 fw-bold"
              disabled={loading || !file}
            >
              {loading ? "Uploading..." : "Upload Activity"}
            </button>
          </form>
        </div>
      </div>

      {#if uploads.length > 0}
        <div class="card bg-dark text-white border-secondary shadow">
          <div class="card-header border-secondary bg-transparent py-3">
            <h2 class="h5 mb-0">Recent Uploads</h2>
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
  :global(body) {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    min-height: 100vh;
  }

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
