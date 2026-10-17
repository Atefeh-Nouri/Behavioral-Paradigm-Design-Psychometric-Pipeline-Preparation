# ==============================================================================
# renv Activation Bootstrap Script
# Ensures that R sessions running in analysis_r reference the project-local library.
# ==============================================================================

local({
  project_root <- normalizePath(getwd(), winslash = "/", mustWork = FALSE)
  
  # Locate renv library path within project boundary
  renv_root <- if (dir.exists(file.path(project_root, "analysis_r/renv"))) {
    file.path(project_root, "analysis_r/renv")
  } else if (dir.exists(file.path(project_root, "renv"))) {
    file.path(project_root, "renv")
  } else {
    NULL
  }

  if (!is.null(renv_root)) {
    r_ver <- paste(R.version$major, substr(R.version$minor, 1, 1), sep = ".")
    lib_path <- file.path(renv_root, "library", R.version$platform, r_ver)
    
    if (dir.exists(lib_path)) {
      .libPaths(c(lib_path, .libPaths()))
      message("renv: Activated project library at ", lib_path)
    } else {
      message("renv: Local library path not yet initialized. Run renv::restore() to synchronize.")
    }
  }
})
